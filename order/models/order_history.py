from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from helper.choice_helpers import find_verbose_type_from_choices
from order.constants.order_history_types import ORDER_HISTORY_TYPE_CHOICES
from order.models import Order


class OrderHistory(RandomIDModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_histories")
    type = models.CharField(max_length=2, choices=ORDER_HISTORY_TYPE_CHOICES)
    message = models.TextField(null=True, blank=True)
    old_obj = JSONField()
    new_obj = JSONField()
    is_approved = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_history"
        ordering = ["-id", "-order_id"]

    @property
    def verbose_type(self):
        return find_verbose_type_from_choices(ORDER_HISTORY_TYPE_CHOICES, self.type)
