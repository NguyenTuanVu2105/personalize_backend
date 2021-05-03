import os

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import GenericViewSet
from order.constants.fulfillment_tracking_statuses import FULFILLMENT_ORDER_PACK_TRACKING_STATUS_VERBOSE_DICT
from order.models import OrderTracker, FulfillmentOrderPack
from order.serializers import OrderTrackerSerializer
import logging

from order.services.order_pack_tracking_scan import update_order_pack_tracking
from service_communication.constants.incoming_webhook_types import IncomingWebhookType
from service_communication.services.fulfill_tracking_service import update_tracking_history
from service_communication.views.generic_incoming_webhook_handle import GenericIncomingWebhookHandle

logger = logging.getLogger(__name__)


class TrackingToolServiceView(GenericViewSet, GenericIncomingWebhookHandle):
    permission_classes = [permissions.AllowAny, ]
    queryset = OrderTracker.objects.all()
    serializer_class = OrderTrackerSerializer
    base_tracking_url = os.environ.get("CLIENT_URL") + "/tracking/{}"

    @action(url_path='tracker-update', detail=False, methods=["POST"])
    def tracker_update(self, request, *args, **kwargs):
        request_data = request.data
        incoming_webhook = self.save_webhook(request_data=request_data,
                                             webhook_type=IncomingWebhookType.TRACKING_TOOL_UPDATE_TRACKER)
        if "tracking_code" in request_data:
            tracking_code = request_data["tracking_code"]
            fulfillment_order_packs = FulfillmentOrderPack.objects.filter(tracking_number=tracking_code)
            order = fulfillment_order_packs.first().order_pack.order
            incoming_webhook.relate_object = order
            incoming_webhook.save()
            status, carrier, tracking_url = self.parse_tracking_data(request_data)
            update_tracking_history(tracking_code, request_data)
            for fulfillment_order_pack_obj in fulfillment_order_packs:
                update_order_pack_tracking(fulfillment_order_pack_obj, status, carrier, tracking_url)
            self.handle_webhook_success(incoming_webhook)
        else:
            self.handle_webhook_error(incoming_webhook, "")
        return Response({"success": True})

    def parse_tracking_data(self, tracking_data):
        status = FULFILLMENT_ORDER_PACK_TRACKING_STATUS_VERBOSE_DICT[tracking_data["status"]]
        tracking_url = self.base_tracking_url.format(tracking_data["tracking_code"])
        carrier = tracking_data["carrier"]
        return status, carrier, tracking_url
