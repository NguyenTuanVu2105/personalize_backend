from django.db import models

from HUB import settings
from HUB.models.mixins.custom_save import CustomizedSavingModelMixin
from HUB.models.random_id_model import RandomIDModel


class SampleShippingAddress(CustomizedSavingModelMixin, RandomIDModel):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    apartment = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "sample_shipping_address"
