import datetime
import os

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from notification.enums.message_types import MessageType
from notification.models import Template
from notification.services.notification import send_user_email
from user.functions.email_token_generator import forgot_password_token

User = get_user_model()
utc = pytz.UTC

RESET_PASSWORD_LINK_FORMAT = "{0}/reset-password/{1}/{2}"


def send_forgot_password_email(user_id, user_email):
    user = User.objects.get(id=user_id)
    client_site = os.environ.get("CLIENT_URL")
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = forgot_password_token.make_token(user)

    now = datetime.datetime.now()
    now = utc.localize(now)
    cnow = now.replace(tzinfo=utc)
    expired_time = cnow + datetime.timedelta(seconds=settings.EXPIRED_FORGOT_PASSWORD_TOKEN_TIME)

    user.token_forgot_password = token
    user.token_forgot_password_expire_time = expired_time
    user.save()

    reset_password_link = RESET_PASSWORD_LINK_FORMAT.format(client_site, uid, token)
    email_data = {
        "mail_title_include": user.name if user.name else user.email + " - PrintHolo",
        "mail_content_include": reset_password_link
    }

    template = Template.objects.get(pk=MessageType.FORGOT_PASSWORD_EMAIL)
    send_user_email(user, template, email_data, [user_email], send_html=True)
