import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model

from notification.enums.message_types import MessageType
from notification.services.notification import send_notification_task, send_notification

User = get_user_model()
utc = pytz.UTC


def send_failed_payment_notification(user_id):
    user = User.objects.get(id=user_id)
    now = datetime.datetime.now()
    now = utc.localize(now)
    cnow = now.replace(tzinfo=utc)
    last_send_failed_payment_notification = user.last_send_failed_payment_noti
    should_send_notification = False
    if last_send_failed_payment_notification:
        time_point_to_send = last_send_failed_payment_notification + datetime.timedelta(
            seconds=settings.TIME_TO_SEND_FAILED_PAYMENT_NOTIFICATIONS)
        if cnow >= time_point_to_send:
            should_send_notification = True
    else:
        should_send_notification = True

    if should_send_notification:
        notification_data = {
            "mail_title_include": user.name if user.name else user.email,
            "mail_content_include": ""
        }
        send_notification_task(user_id, MessageType.RECHARGE_NOTIFICATION, notification_data)
        now = datetime.datetime.now()
        now = utc.localize(now)
        cnow = now.replace(tzinfo=utc)
        user.last_send_failed_payment_noti = cnow
        user.save()


def send_payment_prompt_notification(user_id):
    send_notification(user_id, MessageType.ADD_PAYMENT_PROMPT, {})
