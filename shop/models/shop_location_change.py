from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from shop.constants.shop_location_type import SHOP_LOCATION_TYPE_CHOICES, ShopLocationType
from shop.models import Shop


class ShopLocationChange(RandomIDModel):
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, related_name="location_change")
    shopify_response = JSONField(default={})
    new_location = models.BigIntegerField(null=True)
    old_location = models.BigIntegerField(null=True)
    type = models.CharField(choices=SHOP_LOCATION_TYPE_CHOICES, max_length=2, default=ShopLocationType.WRONG_LOCATION)
    is_resolve = models.BooleanField(default=False)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop_location_change'
        ordering = ['-create_time']
