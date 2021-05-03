from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from billing.sub_apps.combine_payment.constants import PaymentGateway, VerbosePaymentGateway
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod

User = get_user_model()


class UserStripe(RandomIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_stripe_set')
    customer_code = models.CharField(max_length=512, unique=True)
    card_name = models.CharField(max_length=512)
    type = models.CharField(max_length=50)
    last4 = models.CharField(max_length=5)
    exp_month = models.CharField(max_length=5)
    exp_year = models.CharField(max_length=5)
    country = models.CharField(max_length=20)
    billing_order = models.IntegerField(default=0)
    general_payment_methods = GenericRelation(GeneralPaymentMethod)
    fingerprint = models.CharField(max_length=255, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_stripe_payment_method'
        ordering = ['id']
        # unique_together = ('seller', 'last4')
        verbose_name = _('User Stripe')
        verbose_name_plural = _('User Stripe')

    def __str__(self):
        return "{} | Last4: {}".format(self.verbose_gateway_name, self.last4)

    @property
    def gateway_name(self):
        return PaymentGateway.STRIPE

    @property
    def verbose_gateway_name(self):
        return VerbosePaymentGateway.STRIPE

    def parse_info(self):
        return {
            "gateway": self.verbose_gateway_name,
            "card_name": self.card_name,
            "type": self.type,
            "last4": self.last4,
            "exp_month": self.exp_month.rjust(2, "0"),
            "exp_year": self.exp_year,
            "country": self.country
        }
