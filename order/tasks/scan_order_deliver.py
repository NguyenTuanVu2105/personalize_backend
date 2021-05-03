from order.constants.fulfill_statuses import OrderFulfillStatus
from order.functions.is_all_deliver_order import is_all_deliver_order
from order.models import Order
import logging
logger = logging.getLogger(__name__)

def scan_order_deliver():
    orders = Order.objects.filter(fulfill_status=OrderFulfillStatus.FULFILLED).exclude(is_delivered_order=True)
    for order in orders:
        try:
            if is_all_deliver_order(order):
                order.is_delivered_order = True
                order.save()
        except Exception as e:
            logger.error(e)


