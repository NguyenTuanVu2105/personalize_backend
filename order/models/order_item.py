from django.db import models

from HUB.models.random_id_model import RandomIDModel
from abstract_product.constants import AbstractType
from order.managers import OrderItemManager
from shipping.models import ShippingCostAbstractVariant
from user_product.models import UserVariant, EcommerceUnsyncVariant
from .order import Order
from .order_pack import OrderPack
from ..constants.fulfill_statuses import OrderItemFulfillStatus, ORDER_ITEM_FULFILL_STATUS_CHOICES
from ..constants.fulfill_statuses.order_item_fulfill_statuses import ORDER_ITEM_FULFILL_STATUS_DICT
from ..constants.mapping_statuses import MAPPING_STATUS_CHOICES, MappingStatus


class OrderItem(RandomIDModel):
    order_pack = models.ForeignKey(to=OrderPack, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="items")
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="items")
    item_id = models.CharField(max_length=255)
    fulfill_status = models.CharField(max_length=2, choices=ORDER_ITEM_FULFILL_STATUS_CHOICES,
                                      default=OrderItemFulfillStatus.ACCEPTED)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    base_cost = models.DecimalField(max_digits=11, decimal_places=2, default=0)  # in usd
    discount = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    currency = models.CharField(max_length=30)
    price_in_usd = models.DecimalField(max_digits=11, decimal_places=5)
    mfr_base_cost = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    production_cost = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    extra_cost = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    mapping_status = models.CharField(max_length=1, choices=MAPPING_STATUS_CHOICES,
                                      default=MappingStatus.NOTMAP, blank=True)
    ecommerce_variant = models.ForeignKey(to=EcommerceUnsyncVariant, on_delete=models.CASCADE,
                                          related_name="ecommerce_variant", blank=True, null=True)
    user_variant = models.ForeignKey(to=UserVariant, on_delete=models.CASCADE, related_name="order_items", blank=True,
                                     null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = OrderItemManager()

    class Meta:
        db_table = "order_item"
        ordering = ["id"]

    def __str__(self):
        return "Item ID {} | Customer {}".format(self.id, self.order_pack)

    def get_shipping_cost_abstract_variant_obj(self, shipping_zone, shipping_rate):
        return ShippingCostAbstractVariant.objects.filter(abstract_variant_sku=self.user_variant.abstract_variant.sku,
                                                          shipping_zone=shipping_zone,
                                                          shipping_rate=shipping_rate).first()

    def is_shipping_supported(self, *args, **kwargs):
        return bool(self.get_shipping_cost_abstract_variant_obj(*args, **kwargs))

    @property
    def is_branding_card_item(self, *args, **kwargs):
        return bool(self.user_variant.abstract_variant.product.type == AbstractType.THANK_YOU_CARD)

    def set_rejected(self):
        self.fulfill_status = OrderItemFulfillStatus.REJECTED
        self.save()

    @property
    def verbose_fulfill_status(self):
        return ORDER_ITEM_FULFILL_STATUS_DICT.get(self.fulfill_status)
