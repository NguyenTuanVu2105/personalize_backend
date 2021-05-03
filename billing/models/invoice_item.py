from django.db import models

from HUB.models.random_id_model import RandomIDModel
from order.models import OrderItem
from .invoice_pack import InvoicePack


class InvoiceItem(RandomIDModel):
    invoice_pack = models.ForeignKey(to=InvoicePack, on_delete=models.CASCADE, related_name="items")
    order_item = models.ForeignKey(to=OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.BigIntegerField(default=0)
    price = models.DecimalField(decimal_places=2, default=0, max_digits=11, blank=True)
    currency = models.CharField(max_length=30, blank=True, default="USD")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_time']
