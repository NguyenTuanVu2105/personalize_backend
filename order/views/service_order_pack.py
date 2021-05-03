import logging

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from order.constants.fulfillment_tracking_statuses import FULFILLMENT_ORDER_PACK_TRACKING_STATUS_DICT, \
    FulfilmentOrderPackTrackingStatus
from order.models import FulfillmentOrderPack
from order.services.user_order import update_order_cached_metadata_task
from order.tasks import create_order_delivered_notification_task

logger = logging.getLogger(__name__)


class ServiceOrderPackViewSet(ViewSet):
    authentication_classes = {}
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]

    @action(methods=["POST"], detail=False, url_path="tracking")
    def update_order_info(self, request):
        request_data = request.data
        if request_data["description"] == "tracker.updated":
            result = request_data["result"]
            order_packs = FulfillmentOrderPack.objects.filter(tracking_id=result["id"])
            for order_pack in order_packs:
                order_pack.tracking_status = FULFILLMENT_ORDER_PACK_TRACKING_STATUS_DICT[result["status"]]
                order_pack.save(update_fields=['tracking_status'])
                update_order_cached_metadata_task.delay(order_pack.order_pack.order_id)
        return Response({})
