from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from billing.sub_apps.combine_payment.constants import PaymentGateway, VerbosePaymentGateway
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod

User = get_user_model()


class UserPayoneerPaymentMethod(RandomIDModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="payoneer_payment_methods")
    payee_id = models.CharField(max_length=50, db_index=True)
    type = models.CharField(max_length=100, default="INDIVIDUAL", blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    detail = JSONField(blank=True, null=True, default=dict)
    general_payment_methods = GenericRelation(GeneralPaymentMethod)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_payoneer_payment_method'
        ordering = ["-id"]

    @property
    def gateway_name(self):
        return PaymentGateway.PAYONEER

    @property
    def verbose_gateway_name(self):
        return VerbosePaymentGateway.PAYONEER

    def parse_info(self):
        return {
            "gateway": self.verbose_gateway_name,
            "payee": self.payee_id,
            "email": self.email,
            "type": "payoneer",
            "label": "Pay with Payoneer",
            "create_time": self.create_time
        }
