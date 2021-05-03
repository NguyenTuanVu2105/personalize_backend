import logging
from datetime import timedelta

from billing.sub_apps.combine_payment.constants.charge_constants import RETRY_AFTER_MULTI_X_HOURS_PER_FAILED_CHARGE
from billing.sub_apps.combine_payment.functions.send_payment_notification import send_failed_payment_notification
from helper.datetime_helpers import get_current_datetime
from notification.enums.instant_prompt_types import InstantPromptType
from notification.services.instant_prompt import create_instant_prompt, remove_instant_prompt
from user.models import UserSettings

logger = logging.getLogger(__name__)


def process_failed_charge(invoice):
    logger.info(f"PROCESSING FAILED CHARGE Invoice={invoice.id}")
    user_setting = UserSettings.objects.get(user_id=invoice.customer_id)
    invoice.set_failed()
    update_user_setting_on_failed_charge(user_setting)
    logger.info(f"PROCESSED FAILED CHARGE Invoice={invoice.id}")


def update_user_setting_on_failed_charge(user_setting):
    current_datetime = get_current_datetime()
    if user_setting.just_had_some_failed_charges:
        return
    user_id = user_setting.user_id
    user_setting.failed_charge_count += 1
    if user_setting.should_send_failed_notification:
        send_failed_payment_notification(user_id)
    if user_setting.should_halt_to_charge_invoices:
        user_setting.next_charge_time = current_datetime + timedelta(days=100000)
    else:
        user_setting.next_charge_time = current_datetime + timedelta(
            hours=pow(2, user_setting.failed_charge_count) * RETRY_AFTER_MULTI_X_HOURS_PER_FAILED_CHARGE)
    create_instant_prompt(user_id, InstantPromptType.BILLING_CHARGE_FAILED)
    user_setting.save()


def process_success_charge(invoice):
    user_setting = UserSettings.objects.get(user_id=invoice.customer_id)
    invoice.set_paid()
    update_user_setting_on_succeed_charge(user_setting)
    logger.info(f"PROCESSED SUCCESS CHARGE: Invoice={invoice.id}")


def process_canceled_charge(invoice):
    invoice.set_canceled()
    logger.info(f"PROCESSED CANCELED CHARGE: Invoice={invoice.id}")


def update_user_setting_on_succeed_charge(user_setting):
    user_setting.failed_charge_count = 0
    remove_instant_prompt(user_setting.user_id, [InstantPromptType.BILLING_CHARGE_FAILED])
    user_setting.save()


def process_pending_charge(invoice):
    invoice.set_transaction_pending()
    logger.info(f"PROCESSED TRANSACTION_PENDING: Invoice={invoice.id}")
