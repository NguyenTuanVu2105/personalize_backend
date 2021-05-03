from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from billing.sub_apps.combine_payment.constants import PaymentGateway, VerbosePaymentGateway
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod

User = get_user_model()


class PaypalPaymentMethod(RandomIDModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="paypal_payment_methods")
    type = models.CharField(max_length=50, default="pay_pal_account", blank=True, db_index=True)
    payer_id = models.CharField(max_length=15, db_index=True)
    email = models.EmailField()
    agreement_id = models.CharField(max_length=30, unique=True)
    general_payment_methods = GenericRelation(GeneralPaymentMethod)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_paypal_payment_method'
        ordering = ["-id"]

    def __str__(self):
        return "{} | Email: {}".format(self.verbose_gateway_name, self.email)

    @property
    def gateway_name(self):
        return PaymentGateway.PAYPAL_PRO

    @property
    def verbose_gateway_name(self):
        return VerbosePaymentGateway.PAYPAL_PRO

    def parse_info(self):
        return {
            "gateway": self.verbose_gateway_name,
            "type": self.type,
            "email": self.email,
            "create_time":self.create_time
        }
