from django.db.models import ForeignKey, CharField, CASCADE

from HUB.models.random_id_model import RandomIDModel
from order.models import Order


class OrderMappingSkuLog(RandomIDModel):
    order = ForeignKey(to=Order, on_delete=CASCADE)
    ph_product_sku = CharField(max_length=255, null=True)
    note = CharField(max_length=1000)

    class Meta:
        ordering = ['id']
        db_table = 'order_mapping_sku_log'
