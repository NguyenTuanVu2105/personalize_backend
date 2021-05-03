from django.db import models

from HUB.models.mixins.custom_save import CustomizedSavingModelMixin
from HUB.models.random_id_model import RandomIDModel


class OrderShippingAddress(CustomizedSavingModelMixin, RandomIDModel):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.TextField(null=True, blank=True)
    address2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_shipping_address"

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __eq__(self, other):
        values = [(k, v) for k, v in self.__dict__.items() if k != '_state']
        other_values = other and [(k, v) for k, v in other.__dict__.items() if k != '_state']
        return values == other_values

    def check_if_data_has_changed(self):
        old_shipping_address_obj = OrderShippingAddress.objects.filter(id=self.id).select_related("order").first()
        return old_shipping_address_obj != self, old_shipping_address_obj.country_code != self.country_code, old_shipping_address_obj
