from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from billing.sub_apps.combine_payment.constants import PaymentGateway, VerbosePaymentGateway
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod

User = get_user_model()


class PaypalVaultPaymentMethod(RandomIDModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="paypal_vault_payment_methods")
    payment_token = models.CharField(max_length=30)
    card_name = models.CharField(max_length=512, blank=True, null=True)
    type = models.CharField(max_length=30, db_index=True)
    last4 = models.CharField(max_length=5)
    exp_month = models.CharField(max_length=5)
    exp_year = models.CharField(max_length=5)
    general_payment_methods = GenericRelation(GeneralPaymentMethod)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_paypal_vault_payment_method'
        ordering = ["-id"]

    def __str__(self):
        return "{} | Last4: {}".format(self.verbose_gateway_name, self.last4)

    @property
    def gateway_name(self):
        return PaymentGateway.PAYPAL_VAULT

    @property
    def verbose_gateway_name(self):
        return VerbosePaymentGateway.PAYPAL_VAULT

    def parse_info(self):
        return {
            "gateway": self.verbose_gateway_name,
            "type": self.type,
            "last4": self.last4,
            "exp_month": self.exp_month.rjust(2, "0"),
            "exp_year": self.exp_year,
            "create_time": self.create_time
        }
