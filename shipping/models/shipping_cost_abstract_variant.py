from django.db import models

from HUB.models.random_id_model import RandomIDModel
from shipping.models.shipping_rate import ShippingRate
from shipping.models.shipping_zone import ShippingZone


class ShippingCostAbstractVariant(RandomIDModel):
    abstract_variant_sku = models.CharField(max_length=100, default='', db_index=True)
    shipping_zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE)
    shipping_rate = models.ForeignKey(ShippingRate, on_delete=models.CASCADE)
    shipping_cost_base = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    shipping_cost_additional = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    production_cost_base = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    production_cost_additional = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shipping_cost_abstract_variant'
        ordering = ['update_time', 'create_time']

