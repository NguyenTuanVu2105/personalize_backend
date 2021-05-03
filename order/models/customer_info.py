from django.db import models

from HUB.models.random_id_model import RandomIDModel


class CustomerInfo(RandomIDModel):
    customer_id = models.BigIntegerField(null=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_customer_info"

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
