from django.db import transaction

from order.constants.fulfill_statuses import OrderItemFulfillStatus, OrderPackFulfillStatus
from order.models import OrderPack
from order.services.order_status import update_order_static_fulfill_status


def get_order_pack_fulfill_status(order_pack_obj):
    item_fulfill_statuses = order_pack_obj.item_fulfill_statuses
    if OrderItemFulfillStatus.ACCEPTED in item_fulfill_statuses:
        return order_pack_obj.fulfill_status
    elif OrderItemFulfillStatus.HOLDING in item_fulfill_statuses:
        return order_pack_obj.fulfill_status
    else:
        return OrderPackFulfillStatus.REJECTED


@transaction.atomic
def update_order_pack_static_fulfill_status(order_pack_obj, force_reload_order_pack_obj=True):
    if force_reload_order_pack_obj:
        order_pack_obj = OrderPack.objects.include_item_fulfill_statuses().filter(pk=order_pack_obj.pk).first()
    old_fulfill_status = order_pack_obj.fulfill_status
    new_fulfill_status = get_order_pack_fulfill_status(order_pack_obj)
    if new_fulfill_status != old_fulfill_status:
        order_pack_obj.fulfill_status = new_fulfill_status
        order_pack_obj.save()


@transaction.atomic
def update_order_packs_static_fulfill_status(order_obj, updated_pack_objs):
    for pack_obj in updated_pack_objs:
        update_order_pack_static_fulfill_status(pack_obj)
    update_order_static_fulfill_status(order_obj)
