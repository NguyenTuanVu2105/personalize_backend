from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from order.models import Order
from order.services.order_history import create_order_history_for_new_order, \
    create_order_history_for_shipping_rate_change
from system_metadata.services.currency_converter import convert_local_money_to_usd


@receiver([pre_save, ], sender=Order)
def update_order_total_price_in_usd(sender, instance, **kwargs):
    total_price = instance.total_price
    if total_price is not None:
        total_price_in_usd = convert_local_money_to_usd(total_price, instance.currency)
        total_price_in_usd = round(total_price_in_usd, 5)
        previous_total_price_in_usd = instance.total_price_in_usd
        if total_price_in_usd != previous_total_price_in_usd:
            instance.total_price_in_usd = total_price_in_usd


@receiver([pre_save, ], sender=Order)
def update_shipping_rate(sender, instance, **kwargs):
    new_order_obj = instance
    id = new_order_obj.pk
    if not id:
        return
    old_order_obj = Order.objects.filter(id=id).first()
    if old_order_obj:
        if new_order_obj.shipping_rate_id != old_order_obj.shipping_rate_id:
            create_order_history_for_shipping_rate_change(new_order_obj, old_order_obj.shipping_rate.name,
                                                          new_order_obj.shipping_rate.name)


@receiver([post_save, ], sender=Order)
def create_order_history(sender, instance, created, **kwargs):
    if created:
        create_order_history_for_new_order(instance)
