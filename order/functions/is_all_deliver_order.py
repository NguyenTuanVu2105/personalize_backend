from django.db.models import Q

from order.constants.fulfillment_tracking_statuses import FulfilmentOrderPackTrackingStatus
from order.models import FulfillmentOrderPack


def is_all_deliver_order(order):
    return not FulfillmentOrderPack.objects.filter(order_pack__order_id=order.id).filter(
            ~Q(tracking_status=FulfilmentOrderPackTrackingStatus.DELIVERED)).exists()