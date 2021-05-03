from django.db.models.signals import post_save
from django.dispatch import receiver

from billing.sub_apps.combine_payment.functions import create_general_payment_method
from billing.sub_apps.stripe_payment.models import UserStripe


@receiver([post_save, ], sender=UserStripe)
def save_payment_method(sender, instance, created, **kwargs):
    if created:
        create_general_payment_method(instance)
