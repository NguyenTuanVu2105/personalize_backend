from datetime import timedelta

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from helper.choice_helpers import find_verbose_type_from_choices
from order.constants.financial_statuses import ORDER_FINANCIAL_STATUS_CHOICES, OrderFinancialStatus
from order.constants.fulfill_statuses import OrderFulfillStatus, ORDER_FULFILL_STATUS_CHOICES
from order.constants.order_types import ORDER_TYPE_CHOICES, OrderTypes
from order.managers import OrderManager
from order.models.shipping_address import OrderShippingAddress
from shipping.models import ShippingRate, ShippingCountry
from shop.models import Shop
from support.models.support_ticket_target import SupportTicketTarget
from user.contants.time_delays import EDIT_ORDER_ITEMS_DELAY
from .customer_info import CustomerInfo
from ..constants.financial_statuses import ORDER_FINANCIAL_STATUSES_CANCELLABLE
from ..constants.fulfill_statuses import ORDER_STATUSES_ALLOW_UPDATE_SHIPPING, ORDER_FULFILL_STATUSES_CANCELLABLE
from ..constants.fulfill_statuses.order_fulfill_statuses import ORDER_STATUSES_ALLOW_UPDATE_ITEM
from ..constants.fulfillment_tracking_statuses import FulfilmentOrderPackTrackingStatus


def cached_metadata():
    return {
        "packs": []
    }


def get_verbose_fulfill_status(fulfill_status):
    return find_verbose_type_from_choices(ORDER_FULFILL_STATUS_CHOICES, fulfill_status)


def get_verbose_financial_status(financial_status):
    return find_verbose_type_from_choices(ORDER_FINANCIAL_STATUS_CHOICES, financial_status)


class Order(RandomIDModel):
    order_id = models.CharField(max_length=20, unique=True, null=True)
    order_number = models.CharField(max_length=20, default=0, null=True)
    note = models.TextField(null=True, blank=True)
    fulfill_status = models.CharField(max_length=2, choices=ORDER_FULFILL_STATUS_CHOICES,
                                      default=OrderFulfillStatus.UNFULFILLED, blank=True)
    financial_status = models.CharField(max_length=2, choices=ORDER_FINANCIAL_STATUS_CHOICES,
                                        default=OrderFinancialStatus.PENDING, blank=True)
    total_price_in_usd = models.DecimalField(max_digits=11, decimal_places=5)
    total_price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=5, default='USD')
    customer_info = models.OneToOneField(to=CustomerInfo, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.OneToOneField(to=OrderShippingAddress, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    total_items = models.IntegerField(default=0)
    tags = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True)

    tsv_metadata_search = SearchVectorField(null=True)

    shipping_rate = models.ForeignKey(to=ShippingRate, on_delete=models.SET_DEFAULT, default=2, related_name="orders")
    e_commerce_shipping_lines = ArrayField(JSONField(), default=list)

    send_support_email_time = models.DateTimeField(null=True)

    cached_metadata = JSONField(default=cached_metadata)

    support_ticket_targets = GenericRelation(SupportTicketTarget)

    unresolved_support_ticket_count = models.SmallIntegerField(default=0)

    support_ticket_count = models.SmallIntegerField(default=0)

    shipping_cost = models.DecimalField(decimal_places=2, max_digits=11, blank=True, null=True)
    production_cost = models.DecimalField(decimal_places=2, max_digits=11, blank=True, null=True)
    discount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    total_cost = models.DecimalField(decimal_places=2, max_digits=11, blank=True, null=True)
    # fulfillment cost ( PrintHolo profit = total_cost - total_mfr_cost)
    total_mfr_cost = models.DecimalField(decimal_places=2, max_digits=11, blank=True, null=True)
    type = models.CharField(max_length=2, choices=ORDER_TYPE_CHOICES, default=OrderTypes.SHOPIFY)

    seller_edit_time = models.DateTimeField(null=True)
    is_delivered_order = models.BooleanField(default=False)  # manual check
    is_send_mail_add_payment = models.BooleanField(default=False)

    edit_order_items_delay = models.DurationField(default=timedelta(seconds=EDIT_ORDER_ITEMS_DELAY))
    request_order_processing_manually = models.BooleanField(default=False)

    objects = OrderManager()

    class Meta:
        db_table = "order"
        ordering = ["-create_time"]
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    @property
    def verbose_fulfill_status(self):
        return get_verbose_fulfill_status(self.fulfill_status)

    @property
    def verbose_financial_status(self):
        return get_verbose_financial_status(self.financial_status)

    @property
    def is_cancellable(self):
        return self.fulfill_status in ORDER_FULFILL_STATUSES_CANCELLABLE and self.financial_status in ORDER_FINANCIAL_STATUSES_CANCELLABLE

    @property
    def is_shipping_address_editable(self):
        return self.fulfill_status in ORDER_STATUSES_ALLOW_UPDATE_SHIPPING

    @property
    def is_shipping_city_editable(self):
        return self.fulfill_status in ORDER_STATUSES_ALLOW_UPDATE_SHIPPING and not self.has_invoice()

    @property
    def is_shipping_rate_editable(self):
        return self.is_item_editable

    def get_fulfillable_item(self):
        return self.items.accepted_fulfillment()

    @property
    def is_item_editable(self):
        return self.fulfill_status in ORDER_STATUSES_ALLOW_UPDATE_ITEM and not self.has_invoice()

    @property
    def is_item_addable(self):
        return self.fulfill_status in ORDER_STATUSES_ALLOW_UPDATE_ITEM and not self.has_invoice()

    @property
    def is_coupon_editable(self):
        return self.fulfill_status == OrderFulfillStatus.UNFULFILLED

    @property
    def can_request_fulfillment(self):
        return self.fulfill_status == OrderFulfillStatus.UNFULFILLED and not self.has_invoice()

    @property
    def is_pushed_to_fulfillment(self):
        return self.fulfill_status not in (OrderFulfillStatus.UNFULFILLED, OrderFulfillStatus.PENDING)

    def __str__(self):
        return "Order ID {} | Customer {}".format(self.id, self.customer_info)

    def get_shipping_info(self):
        shipping_zone = ''
        if self.shipping_address.country_code:
            shipping_zone = ShippingCountry.objects.filter(code=self.shipping_address.country_code).first().zone
        shipping_rate = self.shipping_rate
        return shipping_zone, shipping_rate

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

    def is_shipping(self):
        return not self.is_delivered() and self.fulfill_status == OrderFulfillStatus.FULFILLED

    def is_delivered(self):
        count = Order.objects \
            .filter(id=self.id) \
            .filter(packs__fulfillment_order_packs__tracking_status=FulfilmentOrderPackTrackingStatus.DELIVERED) \
            .count()
        return count > 0

    def has_invoice(self):
        for pack in self.packs.all():
            if hasattr(pack, 'invoice_pack'):
                return True
        return False

    @property
    def has_branding_card_item(self, *args, **kwargs):
        from abstract_product.constants import AbstractType
        return self.items.filter(user_variant__abstract_variant__product__type=AbstractType.THANK_YOU_CARD).exists()
