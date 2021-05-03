import logging
from datetime import datetime, timedelta

from HUB.settings.notification_setting import CLEAR_MAIL_HISTORY_DAYS
from notification.enums.message_types import MESSAGE_TYPE_DO_NOT_CLEAR
from notification.models import MailHistory

logger = logging.getLogger(__name__)


def clear_mail_history():
    try:
        histories = MailHistory.objects.filter(create_time__lte=datetime.now() - timedelta(days=CLEAR_MAIL_HISTORY_DAYS)).exclude(type__in=MESSAGE_TYPE_DO_NOT_CLEAR)
        print(histories)
        histories.delete()
    except Exception as e:
        logger.exception(e)
