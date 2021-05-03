from django.contrib.auth import get_user_model
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from order.constants.cancel_shipping_request_statuses import CANCEL_SHIPPING_REQUEST_STATUS_CHOICES, \
    CancelShippingRequestStatus
from order.managers import CancelShippingRequestManager
from order.models import Order, OrderPack

User = get_user_model()


class CancelShippingRequest(RandomIDModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="cancel_shipping_requests")
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="cancel_shipping_requests", null=True, blank=True)
    order_packs = models.ManyToManyField(to=OrderPack, related_name="cancel_shipping_requests")
    admin = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="approved_cancel_shipping_requests",
                              null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    admin_note = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=CANCEL_SHIPPING_REQUEST_STATUS_CHOICES,
                              default=CancelShippingRequestStatus.PENDING)
    approve_time = models.DateTimeField(auto_now_add=False, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = CancelShippingRequestManager()

    class Meta:
        db_table = "order_cancel_shipping_request"
        ordering = ["-create_time"]

    @property
    def verbose_status(self):
        current_status = self.status
        for status_choice in CANCEL_SHIPPING_REQUEST_STATUS_CHOICES:
            short_status, verbose_status = status_choice
            if short_status == current_status:
                return verbose_status

    def get_total_shipping_cost(self):
        return self.total_shipping_cost

    @property
    def is_pending(self):
        return self.status == CancelShippingRequestStatus.PENDING

    def __str__(self):
        return "Cancel shipping request {}".format(self.id)
