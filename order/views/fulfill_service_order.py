import logging

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from HUB.permissions.permissions import HeaderBaseAuthentication
from HUB.viewsets.base import GenericViewSet
from order.models import Order
from order.serializers import OrderSerializer
from order.services import update_order_pack_tracking
from order.services.service_order import process_order, reject_order
from service_communication.constants.authenticated_service import AuthenticatedService
from service_communication.constants.incoming_webhook_types import IncomingWebhookType
from service_communication.views.generic_incoming_webhook_handle import GenericIncomingWebhookHandle

logger = logging.getLogger(__name__)


class OrderFulfillServiceViewSet(mixins.CreateModelMixin,
                                 GenericViewSet,
                                 GenericIncomingWebhookHandle):
    authentication_classes = []
    permission_classes = [HeaderBaseAuthentication]
    service_name = AuthenticatedService.FULFILLMENT
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    error_messages = {
        "order": {
            "invalid": "The order is invalid",
            "existed": "The order is existed",
        },
        "shop": {
            "invalid": "This shop is invalid",
        },
    }

    @action(methods=["POST"], detail=False, url_path="process")
    def process_order(self, request):
        return self.update_order(request, process_order, IncomingWebhookType.FULFILL_PROCESS_ORDER)

    @action(methods=["POST"], detail=False, url_path="reject")
    def reject_order(self, request):
        return self.update_order(request, reject_order, IncomingWebhookType.FULFILL_REJECT_ORDER)

    @action(methods=["POST"], detail=False, url_path="tracking")
    def update_tracking(self, request):
        return self.update_order(request, update_order_pack_tracking, IncomingWebhookType.FULFILL_UPDATE_TRACKING)

    def get_order_obj(self, request_data):
        queryset = self.filter_queryset(self.get_queryset())
        pk = request_data.get("id")
        order = get_object_or_404(queryset, id=pk)
        return order

    def update_order(self, request, handle_update, webhook_type):
        request_data = request.data
        order_obj = self.get_order_obj(request_data)

        incoming_webhook = self.save_webhook(relate_object=order_obj,
                                             request_data=request_data,
                                             webhook_type=webhook_type)
        try:
            handle_update(order_obj, request_data)
            self.handle_webhook_success(incoming_webhook)
        except Exception as e:
            logger.exception(e)
            self.handle_webhook_error(incoming_webhook)

        return Response({"success": True})
