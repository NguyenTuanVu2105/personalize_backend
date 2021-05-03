from django.db import models

from HUB.models.random_id_model import RandomIDModel
from billing.constants.invoice_pack_statuses import INVOICE_PACK_STATUS_CHOICES, InvoicePackStatus
from billing.managers import InvoicePackManager
from helper.choice_helpers import find_verbose_type_from_choices
from order.models import OrderPack
from .invoice import Invoice


class InvoicePack(RandomIDModel):
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name='packs')
    order_pack = models.OneToOneField(to=OrderPack, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="invoice_pack")
    status = models.CharField(max_length=2, choices=INVOICE_PACK_STATUS_CHOICES, default=InvoicePackStatus.UNPAID,
                              db_index=True)

    production_cost = models.DecimalField(decimal_places=2, default=0, max_digits=11, blank=True)
    shipping_cost = models.DecimalField(decimal_places=2, default=0, max_digits=11, blank=True)
    discount = models.DecimalField(decimal_places=2, default=0, max_digits=11)
    tax = models.DecimalField(decimal_places=2, default=0, max_digits=11)
    currency = models.CharField(max_length=30, blank=True, default="USD")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = InvoicePackManager()

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return max(self.production_cost + self.shipping_cost - self.discount + self.tax, 0)

    @property
    def shop(self):
        return self.order_pack.order.shop

    @property
    def verbose_status(self):
        return find_verbose_type_from_choices(INVOICE_PACK_STATUS_CHOICES, self.status)
