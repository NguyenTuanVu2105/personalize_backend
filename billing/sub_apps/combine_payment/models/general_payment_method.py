from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from billing.sub_apps.combine_payment.managers import GeneralPaymentMethodManager
from user.models import UserSettings


class GeneralPaymentMethod(RandomIDModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user_setting = models.ForeignKey(to=UserSettings, on_delete=models.CASCADE, related_name="payment_methods")
    ordinal_number = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = GeneralPaymentMethodManager()

    class Meta:
        db_table = 'billing_general_payment_method'
        ordering = ['ordinal_number', '-update_time']

    def __str__(self):
        return "User: {} - Gateway: {}".format(self.user_setting.user.email, self.content_object.verbose_gateway_name)

    def save(self, *args, **kwargs):
        if not self.user_setting_id:
            self.user_setting = self.content_object.user.settings
        return super().save(*args, **kwargs)

    @property
    def payment_gateway_method_data(self):
        if self.content_object:
            return self.content_object.parse_info()

    @property
    def payment_gateway(self):
        return self.content_object.gateway_name

    def deactivate(self):
        self.is_active = False
        self.save()
