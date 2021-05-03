from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import JSONField

from HUB.models.random_id_model import RandomIDModel
from order.models import Order
from .coupon import Coupon

User = get_user_model()


class RedeemedCouponTransaction(RandomIDModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="redeemed_coupon_transactions")
    coupon = models.ForeignKey(to=Coupon, on_delete=models.CASCADE, related_name="redeemed_coupon_transactions")
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, unique=True,
                              related_name="redeemed_coupon_transactions", null=True)

    idempotency_key = models.CharField(max_length=60, unique=True, null=False)
    redeemed_detail = JSONField(default=dict)
    redeemed_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "coupon_redeemed_coupon_transaction"
        ordering = ['-id']

    def __str__(self):
        return "Order ID: {} - Coupon ID: {} [User ID: {}]".format(self.order, self.coupon_id, self.user_id)
