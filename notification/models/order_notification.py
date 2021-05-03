from django.db import models

from HUB.models.random_id_model import RandomIDModel
from notification.constants import ORDER_TRACKING_NOTIFICATION_TYPE_CHOICES
from order.models import Order


class OrderTrackingNotification(RandomIDModel):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    receive_email = models.EmailField()

    type = models.CharField(choices=ORDER_TRACKING_NOTIFICATION_TYPE_CHOICES, max_length=1)
    sent_time = models.DateTimeField(default=None, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_order_tracking'
