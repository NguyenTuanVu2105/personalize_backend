from django.db import models

from HUB.models.random_id_model import RandomIDModel
from billing.constants.invoice_statuses import VerboseInvoiceStatus
from order.constants.fulfill_statuses import ORDER_PACK_STATUS_CHOICES, OrderPackFulfillStatus
from order.constants.fulfillment_tracking_statuses import FulfilmentOrderPackTrackingStatus
from order.managers import OrderPackManager
from order.constants.reject_reason_types import REJECT_REASON_TYPE_CHOICES
from .order import Order


class OrderPack(RandomIDModel):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="packs")
    merch_pack_id = models.CharField(max_length=255, null=True, blank=True)
    fulfill_status = models.CharField(max_length=2, choices=ORDER_PACK_STATUS_CHOICES,
                                      default=OrderPackFulfillStatus.UNFULFILLED, blank=True, db_index=True)
    service = models.CharField(max_length=50, blank=True, null=True)
    location_id = models.CharField(max_length=50, blank=True, null=True)
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=11, blank=True, null=True)
    production_cost = models.DecimalField(decimal_places=2, max_digits=11, blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=11, blank=True, default=0)
    total_cost = models.DecimalField(decimal_places=2, max_digits=11, blank=True, null=True)
    currency = models.CharField(max_length=30, blank=True, default="USD")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    reject_reason_type = models.CharField(max_length=2, choices=REJECT_REASON_TYPE_CHOICES,
                                          default=FulfilmentOrderPackTrackingStatus.UNKNOWN, blank=True, null=True)

    objects = OrderPackManager()

    class Meta:
        db_table = "order_pack"
        ordering = ['create_time']

    def __str__(self):
        return "Pack {} | {}".format(self.id, self.order)

    @property
    def is_fulfilled(self):
        return self.fulfill_status == OrderPackFulfillStatus.FULFILLED

    def set_fulfill_status(self, fulfill_status):
        self.fulfill_status = fulfill_status
        self.save(update_fields=['fulfill_status'])

    @property
    def verbose_fulfill_status(self):
        current_fulfill_status = self.fulfill_status
        for status_choice in ORDER_PACK_STATUS_CHOICES:
            short_status, verbose_status = status_choice
            if short_status == current_fulfill_status:
                return verbose_status

    @property
    def verbose_financial_status(self):
        try:
            return self.invoice_pack.verbose_status
        except AttributeError:
            if self.fulfill_status in (OrderPackFulfillStatus.CANCELED, OrderPackFulfillStatus.REJECTED):
                return VerboseInvoiceStatus.CANCELED
            else:
                return VerboseInvoiceStatus.UNPAID

    def update_costs(self, production_cost=None, shipping_cost=None, discount=None):
        production_cost_changed = False
        shipping_cost_changed = False
        discount_changed = False
        if production_cost is not None and self.production_cost != production_cost:
            self.production_cost = production_cost
            production_cost_changed = True
        if shipping_cost is not None and self.shipping_cost != shipping_cost:
            self.shipping_cost = shipping_cost
            shipping_cost_changed = True
        if discount is not None and self.discount != discount:
            self.discount = discount
            discount_changed = True
        if production_cost_changed or shipping_cost_changed or discount_changed:
            self.total_cost = max(self.production_cost + self.shipping_cost - self.discount, 0)
            self.save()
