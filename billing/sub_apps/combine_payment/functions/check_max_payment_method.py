import logging

from django.contrib.contenttypes.models import ContentType

from HUB import settings
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod
from billing.sub_apps.payoneer_payment.models import UserPayoneerPaymentMethod
from user.models import UserSettings

logger = logging.getLogger(__name__)


def check_max_user_payment_method(user, payment_model):
    payment_count = GeneralPaymentMethod.objects.filter(user_setting=UserSettings.objects.get(user=user),
                                                        content_type=ContentType.objects.get_for_model(
                                                            payment_model), is_active=True).count()
    logger.info(payment_count)
    return payment_count >= settings.MAX_PAYMENT_METHODS_PER_PAYMENT_GATEWAY
