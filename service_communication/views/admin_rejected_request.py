from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from service_communication.constants.rejected_request_statuses import REJECTED_REQUEST_STATUS_CHOICES
from service_communication.constants.request_type import REQUEST_TYPES
from service_communication.models import RejectedRequest
from service_communication.serializers.rejected_request import RequestRejectedSerializer
from service_communication.services.rejected_request import confirm_rejected_request, resolve_rejected_request


class AdminRejectedRequestViewSet(SearchableListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  AdminGenericViewSet):
    queryset = RejectedRequest.objects.all()
    serializer_class = RequestRejectedSerializer
    filterset_fields = ('request_type', 'status')

    error_messages = {
        "status": {
            "invalid": "You can only process pending order",
        }
    }

    def get_queryset(self):
        return self.queryset.prefetch_related("relate_object")

    def get_options(self):
        return {
            'request_type': REQUEST_TYPES,
            'status': REJECTED_REQUEST_STATUS_CHOICES
        }

    @method_permission_required(get_permissions(['admin_order_view', ]))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['options'] = self.get_options()
        return response

    @action(methods=["POST"], detail=True, url_path="resolve")
    def resolve(self, request, *args, **kwargs):
        return self.handle_request(request, resolve_rejected_request)

    @action(methods=["POST"], detail=True, url_path="reject")
    def reject(self, request, *args, **kwargs):
        return self.handle_request(request, confirm_rejected_request)

    def handle_request(self, request, handle_request):
        request_data = request.data
        cancel_shipping_request = self.get_object()
        handle_request(request.user, cancel_shipping_request, request_data)
        return Response({"success": True})
