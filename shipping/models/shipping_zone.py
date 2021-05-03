from django.db import models

from HUB.models.random_id_model import RandomIDModel


class ShippingZone(RandomIDModel):
    name = models.CharField(max_length=31)
    description = models.CharField(max_length=1023)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shipping_zone'
        ordering = ['update_time', 'create_time']

