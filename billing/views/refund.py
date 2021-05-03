from django.core.exceptions import ValidationError
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from billing.constants.refund_statuses import RefundStatus
from billing.models import Refund
from billing.serializers.refund import AdminRefundSerializer
from billing.services.refund import create_manual_refund
from helper.datetime_helpers import get_current_datetime


class AdminRefundViewSet(SearchableListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         AdminGenericViewSet):
    queryset = Refund.objects.all()
    serializer_class = AdminRefundSerializer

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_refund_view', ]))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_permission_required(get_permissions(['admin_refund_update', ]))
    def create(self, request, *args, **kwargs):
        try:
            create_manual_refund(request.data)
        except ValidationError as e:
            return Response({"success": False, "errors": e.message_dict})
        else:
            return Response({"success": True})

    @action(methods=["POST"], detail=True, url_path="retry",
            permission_classes=get_permissions(['admin_refund_update', ]))
    def retry(self, request, *args, **kwargs):
        refund_obj = self.get_object()
        if not refund_obj.is_retryable:
            return Response({"success": False, "description": "Status not match"})
        refund_obj.set_status(RefundStatus.PENDING)
        refund_obj.save()
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="retry_all",
            permission_classes=get_permissions(['admin_refund_update', ]))
    def retry_all(self, request):
        self.queryset.filter(status=RefundStatus.FAILED).update(status=RefundStatus.PENDING)
        return Response({"success": True})

    @action(methods=["POST"], detail=True, url_path="approve",
            permission_classes=get_permissions(['admin_refund_update', ]))
    def approve(self, request, *args, **kwargs):
        return self.handle_refund_approve_request(request, status=RefundStatus.PENDING)

    @action(methods=["POST"], detail=True, url_path="reject",
            permission_classes=get_permissions(['admin_refund_update', ]))
    def reject(self, request, *args, **kwargs):
        return self.handle_refund_approve_request(request, status=RefundStatus.REJECTED)

    def handle_refund_approve_request(self, request, status):
        refund_obj = self.get_object()
        if refund_obj.is_approvable:
            refund_obj.approve_time = get_current_datetime()
            refund_obj.set_status(status)
            return Response({"success": True})
        return Response({"success": False})
