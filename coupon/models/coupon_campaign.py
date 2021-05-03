from django.db import models

from HUB.models.random_id_model import RandomIDModel


class CouponCampaign(RandomIDModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "coupon_campaign"
        ordering = ['id']

    def __str__(self):
        return self.name
