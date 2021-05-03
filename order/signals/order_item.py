import logging

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from order.models import OrderItem
from order.services.order_history import create_order_history_for_order_item_quantity_change, \
    create_order_history_for_order_item_user_variant_change, create_order_history_for_order_item_remove
from system_metadata.services.currency_converter import convert_local_money_to_usd

logger = logging.getLogger(__name__)


@receiver([pre_save, ], sender=OrderItem)
def update_order_item(sender, instance, **kwargs):
    new_order_item_obj = instance
    id = new_order_item_obj.pk
    if not id:
        return
    old_order_item_obj = OrderItem.objects.filter(id=id).select_related("order").first()
    if old_order_item_obj:
        if new_order_item_obj.quantity != old_order_item_obj.quantity:
            create_order_history_for_order_item_quantity_change(new_order_item_obj.order, old_order_item_obj,
                                                                new_order_item_obj)
        if new_order_item_obj.user_variant_id != old_order_item_obj.user_variant_id:
            create_order_history_for_order_item_user_variant_change(new_order_item_obj.order,
                                                                    old_order_item_obj.user_variant,
                                                                    new_order_item_obj.user_variant)


# @receiver([pre_delete, ], sender=OrderItem)
# def remove_order_item(sender, instance, **kwargs):
#     deleted_order_item_obj = instance
#     order_obj = deleted_order_item_obj.order
#     create_order_history_for_order_item_remove(order_obj=order_obj, order_item_obj=deleted_order_item_obj)


@receiver([pre_save, ], sender=OrderItem)
def update_order_item_price_in_usd(sender, instance, **kwargs):
    price = instance.price
    if price:
        price_in_usd = convert_local_money_to_usd(price, instance.currency)
        price_in_usd = round(price_in_usd, 5)
        previous_price_in_usd = instance.price_in_usd
        if price_in_usd != previous_price_in_usd:
            instance.price_in_usd = price_in_usd
