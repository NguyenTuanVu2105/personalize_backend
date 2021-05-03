from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from shop.models import Shop


class ShopShippingProfile(RandomIDModel):
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, related_name="shipping_profiles")
    profile_id = models.CharField(max_length=100)
    zones_config = JSONField()
    name = models.CharField(max_length=100)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop_shipping_profile'
        ordering = ['-create_time']
