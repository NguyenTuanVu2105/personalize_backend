from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from order.models import CancelShippingRequest
from order.serializers.order_cancel_shipping_request import OrderCancelShippingRequestDetailSerializer
from order.serializers.order_cancel_shipping_request_admin import CancelShippingRequestSerializer
from order.services import approve_cancel_shipping_request, reject_cancel_shipping_request


class OrderCancelShippingRequestViewSet(mixins.ListModelMixin,
                                        AdminGenericViewSet):
    queryset = CancelShippingRequest.objects.all()
    serializer_class = OrderCancelShippingRequestDetailSerializer

    def get_queryset(self):
        return self.queryset.all()

    @method_permission_required(get_permissions(['admin_cancel_shipping_view', ]))
    def list(self, request, *args, **kwargs):
        self.serializer_class = CancelShippingRequestSerializer
        return super().list(request, *args, **kwargs)

    @action(methods=["POST"], detail=True, url_path="approve",
            permission_classes=get_permissions(['admin_cancel_shipping_update', ]))
    def approve(self, request, *args, **kwargs):
        return self.handle_cancel_shipping_request(request, approve_cancel_shipping_request)

    @action(methods=["POST"], detail=True, url_path="reject",
            permission_classes=get_permissions(['admin_cancel_shipping_update', ]))
    def reject(self, request, *args, **kwargs):
        return self.handle_cancel_shipping_request(request, reject_cancel_shipping_request)

    def handle_cancel_shipping_request(self, request, handle_request):
        request_data = request.data
        cancel_shipping_request = self.get_object()
        handle_request(request.user, cancel_shipping_request, request_data)
        return Response({"success": True})
