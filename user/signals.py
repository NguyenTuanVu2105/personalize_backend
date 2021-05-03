import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from billing.sub_apps.braintree_payment.services import create_braintree_customer
from billing.sub_apps.combine_payment.functions.send_payment_notification import send_payment_prompt_notification
from .models import User

logger = logging.getLogger(__name__)


@receiver([post_save, ], sender=User)
def save_user(sender, instance, created, **kwargs):
    if created:
        instance.create_user_settings()
        create_braintree_customer(instance)
        send_payment_prompt_notification(instance.id)
