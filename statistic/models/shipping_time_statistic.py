from django.db import models

from HUB.models.random_id_model import RandomIDModel
from django.utils.translation import gettext as _


class ShippingTimeStatistic(RandomIDModel):
    point = models.DateTimeField()
    average_time = models.DecimalField(decimal_places=2, max_digits=5)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "statistic_shipping_time"
        ordering = ['point', 'id']
        verbose_name = _('Abstract Product Statistic')
        verbose_name_plural = _('Abstract Products Statistic')
