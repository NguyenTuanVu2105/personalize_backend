import datetime
import os

import pytz
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from notification.enums.message_types import MessageType
from notification.models import Template
from notification.services.notification import send_user_email
from user.functions.email_token_generator import account_activation_token

User = get_user_model()
utc = pytz.UTC

ACTIVATION_LINK_FORMAT = "{0}/account-activation/{1}/{2}"

logger = get_task_logger(__name__)


def send_activation_email(user_id):
    user = User.objects.get(id=user_id)
    client_site = os.environ.get("CLIENT_URL")
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    now = datetime.datetime.now()
    now = utc.localize(now)
    cnow = now.replace(tzinfo=utc)
    expired_time = cnow + datetime.timedelta(seconds=settings.EXPIRED_EMAIL_TIME)
    logger.info(user)
    # user.token_confirmation = token
    # user.token_confirmation_expire_time = expired_time
    # user.save()
    User.objects.filter(pk=user_id).update(token_confirmation=token, token_confirmation_expire_time=expired_time)
    activation_link = ACTIVATION_LINK_FORMAT.format(client_site, uid, token)
    logger.info(activation_link)
    email_data = {
        "mail_title_include": user.name if user.name else user.email,
        "user_name": user.name if user.name else user.email,
        "active_link": activation_link
    }

    template = Template.objects.get(pk=MessageType.REGISTRATION_ACTIVATION_EMAIL)
    # logger.info("Token: {}".format(user.token_confirmation))
    send_user_email(user, template, email_data, send_html=True)
