from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from shop.models import Shop


def default_last_order_update_time():
    return timezone.now() - timedelta(days=1)


class OrderScanInfo(RandomIDModel):
    shop = models.OneToOneField(
        Shop,
        on_delete=models.CASCADE,
        related_name="order_scan_info"
    )
    update_time = models.DateTimeField(auto_now=True)
    last_order_update_time = models.DateTimeField(default=default_last_order_update_time)
    checked_order_ids = ArrayField(models.BigIntegerField(), default=list)

    class Meta:
        db_table = 'order_scan_info'
        verbose_name = _('Order Scan Info')
        verbose_name_plural = _('Order Scan Info')
