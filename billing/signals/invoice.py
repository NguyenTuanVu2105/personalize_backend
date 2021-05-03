from django.db.models.signals import post_save
from django.dispatch import receiver

from billing.models import Invoice
from order.models import Order
from order.services.order_status import update_order_static_financial_status


@receiver([post_save, ], sender=Invoice)
def update_order_financial_status(sender, instance, created, **kwargs):
    orders = Order.objects.include_pack_financial_statuses().filter(
        pk__in=instance.packs.values_list("order_pack__order_id", flat=True))
    for order_obj in orders:
        update_order_static_financial_status(order_obj)
