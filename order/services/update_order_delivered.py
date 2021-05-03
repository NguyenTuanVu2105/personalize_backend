from order.functions.is_all_deliver_order import is_all_deliver_order
from order.models import Order


def update_order_delivered(order_id):
     order = Order.objects.get(id=order_id)
     if is_all_deliver_order(order):
          order.is_delivered_order = True
          order.save()