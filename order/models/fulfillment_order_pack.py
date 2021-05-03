from django.db import models

from HUB.models.random_id_model import RandomIDModel
from order.constants.fulfillment_tracking_statuses import FULFILLMENT_ORDER_PACK_TRACKING_STATUS_CHOICES, \
    FulfilmentOrderPackTrackingStatus, VerboseFulfilmentOrderPackTrackingStatus, FULFILLMENT_ORDER_PACK_TRACKING_STATUS_DICT
from order.models import OrderPack


class FulfillmentOrderPack(RandomIDModel):
    order_pack = models.ForeignKey(to=OrderPack, on_delete=models.CASCADE, related_name="fulfillment_order_packs")
    quantity = models.PositiveSmallIntegerField(default=0)
    mfr_pack_id = models.CharField(max_length=255, null=True, blank=True)
    tracking_id = models.CharField(max_length=50, blank=True, null=True)
    tracking_company = models.CharField(max_length=50, blank=True, null=True)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    tracking_url = models.URLField(verbose_name='Tracking Url', blank=True, null=True)
    origin_tracking_url = models.URLField(verbose_name='Origin Tracking Url', blank=True, null=True)
    tracking_status = models.CharField(max_length=2, choices=FULFILLMENT_ORDER_PACK_TRACKING_STATUS_CHOICES,
                                       default=FulfilmentOrderPackTrackingStatus.UNKNOWN)
    manually_update = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True)

    @property
    def verbose_tracking_status(self):
        return FULFILLMENT_ORDER_PACK_TRACKING_STATUS_DICT.get(self.tracking_status, VerboseFulfilmentOrderPackTrackingStatus.UNKNOWN)

    class Meta:
        db_table = "order_fulfillment_pack"
        ordering = ["id"]
