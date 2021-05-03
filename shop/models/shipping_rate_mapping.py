from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from shop.models import Shop
from shipping.models import ShippingRate


class ShopShippingRateMapping(RandomIDModel):
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, related_name="shipping_rate_mappings")
    e_commerce_shipping_rate_name = models.CharField(max_length=255)
    countries = ArrayField(models.CharField(max_length=3), default=list)
    hash_id = models.CharField(max_length=256, default='')
    shipping_rate = models.ForeignKey(to=ShippingRate, on_delete=models.CASCADE, related_name="shop_mappings")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop_shipping_rate_mapping'
        verbose_name = _('Shop Shipping Rate Mapping')
        verbose_name_plural = _('Shop Shipping Rate Mappings')
