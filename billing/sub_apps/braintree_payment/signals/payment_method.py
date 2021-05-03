from django.db.models.signals import post_save
from django.dispatch import receiver

from billing.sub_apps.braintree_payment.models import BraintreePaymentMethod
from billing.sub_apps.combine_payment.functions import create_general_payment_method


@receiver([post_save, ], sender=BraintreePaymentMethod)
def save_payment_method(sender, instance, created, **kwargs):
    if created:
        create_general_payment_method(instance)
