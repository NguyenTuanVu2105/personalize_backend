from django.db import models
from django.contrib.postgres.fields import JSONField
from HUB.models.random_id_model import RandomIDModel


class OrderTracker(RandomIDModel):
    tracking_code = models.CharField(max_length=255, db_index=True)
    payloads = JSONField(default={}, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_tracker"
        ordering = ['-create_time']