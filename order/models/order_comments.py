from django.contrib.postgres.search import SearchVectorField
from django.db import models
from HUB.models.random_id_model import RandomIDModel
from order.models import Order
from user.models import User


class OrderComments(RandomIDModel):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="order_comments", null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True)

    tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = "order_comments"
        ordering = ["-id", "-order_id"]
