from django.db import models

from HUB.models.random_id_model import RandomIDModel
from shipping.models.shipping_zone import ShippingZone


class ShippingCountry(RandomIDModel):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=31)
    # if country support shipping, is_active=true
    is_active = models.BooleanField(default=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name="countries")

    class Meta:
        db_table = 'shipping_country'
        ordering = ['update_time', 'create_time']
