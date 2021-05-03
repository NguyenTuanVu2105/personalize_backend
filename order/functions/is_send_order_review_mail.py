from django.contrib.auth import get_user_model

from notification.enums.mail_history_statuses import MailHistoryStatus
from notification.enums.message_types import MessageType
from notification.models import MailHistory

User = get_user_model()

def is_send_order_review_mail(user_id):
    user = User.objects.get(id=user_id)
    return not MailHistory.objects.filter(owner=user, type=MessageType.ORDER_DELIVERED_REVIEW, status=MailHistoryStatus.SENT).exists()