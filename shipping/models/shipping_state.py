from django.db import models

from HUB.models.random_id_model import RandomIDModel
from shipping.models import ShippingCountry


class ShippingState(RandomIDModel):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    # if country support shipping, is_active=true
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(ShippingCountry, on_delete=models.CASCADE, db_index=True, related_name="states")

    class Meta:
        db_table = 'shipping_state'
        ordering = ['country', 'update_time', 'create_time']
