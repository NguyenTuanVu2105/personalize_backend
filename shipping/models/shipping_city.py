from django.db import models

from HUB.models.random_id_model import RandomIDModel
from shipping.models import ShippingCountry
from shipping.models.shipping_state import ShippingState


class ShippingCity(RandomIDModel):
    name = models.CharField(max_length=50)
    # if country support shipping, is_active=true
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(ShippingCountry, on_delete=models.CASCADE, db_index=True)
    state = models.ForeignKey(ShippingState, on_delete=models.CASCADE, db_index=True,null=True)

    class Meta:
        db_table = 'shipping_city'
        ordering = ['country','state', 'update_time', 'create_time']
