import logging

from django.utils import timezone

from notification.enums.instant_prompt_types import InstantPromptType
from notification.enums.message_statuses import MessageStatus
from notification.models.instant_prompt import InstantPrompt
from support.models import SupportTicket

logger = logging.getLogger(__name__)


def create_instant_prompt(user_id, prompt_type, params=None):
    try:
        InstantPrompt.objects.update_or_create(owner_id=user_id,
                                               type=prompt_type,
                                               defaults={
                                                   "status": MessageStatus.UNREAD,
                                                   "params": params
                                               })
    except Exception as e:
        logger.exception(e)


def generate_default_instant_prompt(user_id):
    try:
        InstantPrompt.objects.bulk_create([
            InstantPrompt(owner_id=user_id, type=InstantPromptType.ADD_SHOP, status=MessageStatus.UNREAD),
            InstantPrompt(owner_id=user_id, type=InstantPromptType.ADD_PAYMENT_METHOD, status=MessageStatus.UNREAD),
            # InstantPrompt(owner_id=user_id, type=InstantPromptType.SHOW_TOUR_NEW_PRODUCT_DESIGN,
            #               status=MessageStatus.UNREAD),
            # InstantPrompt(owner_id=user_id, type=InstantPromptType.SHOW_TOUR_NEW_PRODUCT_PRICING,
            #               status=MessageStatus.UNREAD),
            # InstantPrompt(owner_id=user_id, type=InstantPromptType.SHOW_TOUR_PAYMENT_MANAGER,
            #               status=MessageStatus.UNREAD),
            # InstantPrompt(owner_id=user_id, type=InstantPromptType.SHOW_SHOP_SETTING, status=MessageStatus.UNREAD),
            InstantPrompt(owner_id=user_id, type=InstantPromptType.SHOW_INTRODUCTION, status=MessageStatus.UNREAD),
            InstantPrompt(owner_id=user_id, type=InstantPromptType.ORDER_PROCESSING_TIME, status=MessageStatus.UNREAD),
            InstantPrompt(owner_id=user_id, type=InstantPromptType.POLICY_AGREEMENT, status=MessageStatus.UNREAD)
        ])
    except Exception as e:
        logger.exception(e)


def remove_instant_prompt(user_id, prompt_types):
    try:
        InstantPrompt.objects \
            .filter(owner_id=user_id, type__in=prompt_types) \
            .update(status=MessageStatus.READ, read_time=timezone.now())
    except Exception as e:
        logger.exception(e)


def remove_instant_payment_prompt(user_id):
    remove_instant_prompt(user_id=user_id,
                          prompt_types=[InstantPromptType.ADD_PAYMENT_METHOD, InstantPromptType.BILLING_CHARGE_FAILED])


def remove_instant_ticket_prompt(user_id):
    if not SupportTicket.objects.filter(user_id=user_id, read=False).exists():
        remove_instant_prompt(user_id=user_id,
                              prompt_types=[InstantPromptType.TICKET_UNREAD])
