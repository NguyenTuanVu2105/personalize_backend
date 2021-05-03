from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from order.models import Order


class OrderHolding(RandomIDModel):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="order_holding")
    fulfillment_payload = JSONField()
    printholo_cost = models.DecimalField(max_digits=11, decimal_places=2)
    fulfillment_cost = models.DecimalField(max_digits=11, decimal_places=2)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = "order_holding"
        ordering = ["-id"]
        # indexes = [GinIndex(fields=["tsv_metadata_search"])]