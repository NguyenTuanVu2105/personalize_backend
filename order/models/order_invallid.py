from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from helper.choice_helpers import find_verbose_type_from_choices
from order.constants.invalid_reason_types import INVALID_REASON_TYPE_CHOICES
from order.models import Order
from shop.models import Shop


class OrderInvalid(RandomIDModel):
    order_id = models.CharField(max_length=20, unique=True)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE, related_name="invalid_order", null=True)
    reason_code = models.CharField(max_length=2, choices=INVALID_REASON_TYPE_CHOICES, blank=True)
    reason_description = models.TextField(null=True, blank=True)
    json = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = "order_invalid"
        ordering = ["-id"]
        indexes = [GinIndex(fields=["tsv_metadata_search"])]


    @property
    def verbose_reason_type(self):
        return find_verbose_type_from_choices(INVALID_REASON_TYPE_CHOICES, self.reason_code)