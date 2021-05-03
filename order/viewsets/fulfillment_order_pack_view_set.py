from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from order.constants.fulfillment_tracking_statuses import FulfilmentOrderPackTrackingStatus
from order.models import FulfillmentOrderPack
from order.serializers.fulfillment_order_pack import UpdatableFulfillmentPackSerializer
from order.services.order_pack_tracking_scan import update_order_pack_tracking
from order.services.user_order import update_order_cached_metadata_task
from service_communication.services.fulfill_tracking_service import FulfillTrackingService
import logging
logger = logging.getLogger(__name__)

class AdminFulfillmentOrderPackViewSet(RetrieveModelMixin, ListModelMixin,
                                       UpdateModelMixin, AdminGenericViewSet):
    queryset = FulfillmentOrderPack.objects.all()
    serializer_class = UpdatableFulfillmentPackSerializer
    filterset_fields = ['order_pack', ]

    def update(self, request, *args, **kwargs):
        fulfillment_pack = self.get_object()
        fulfillment_pack_data = super().update(request, *args, **kwargs)
        update_order_cached_metadata_task.delay(fulfillment_pack.order_pack.order_id)
        return fulfillment_pack_data

    @action(methods=['GET'], detail=False, url_path='all')
    def get_all(self, request):
        return Response(self.serializer_class(self.filter_queryset(self.get_queryset()), many=True).data)

    @action(methods=['POST'], detail=True, url_path='sync_tracking')
    def sync_tracking(self, request, *args, **kwargs):
        fulfillment_order_pack_obj = self.get_object()
        status, carrier, tracking_url = FulfillTrackingService.get_tracking(
            fulfillment_order_pack_obj.tracking_number, fulfillment_order_pack_obj.tracking_company)
        if not status == FulfilmentOrderPackTrackingStatus.UNKNOWN:
            update_order_pack_tracking(fulfillment_order_pack_obj=fulfillment_order_pack_obj,
                                       status=status if not status == FulfilmentOrderPackTrackingStatus.UNKNOWN else fulfillment_order_pack_obj.status,
                                       carrier=carrier,
                                       tracking_url=tracking_url)
        return Response({"success": True})

