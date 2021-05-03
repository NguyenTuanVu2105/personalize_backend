from django.db.models.signals import post_save
from django.dispatch import receiver

from billing.sub_apps.combine_payment.functions import create_general_payment_method, reactivate_general_payment_method
from billing.sub_apps.paypal_vault_payment.models import PaypalVaultPaymentMethod


@receiver([post_save, ], sender=PaypalVaultPaymentMethod)
def save_payment_method(sender, instance, created, **kwargs):
    if created:
        create_general_payment_method(instance)
