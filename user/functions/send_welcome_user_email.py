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
from user.functions.email_token_generator import account_activation_token

User = get_user_model()
utc = pytz.UTC

ACTIVATION_LINK_FORMAT = "{0}/account-activation/{1}/{2}"


def send_welcome_user_email(user_id):
    user = User.objects.get(id=user_id)

    email_data = {
        "user_name": user.name if user.name else user.email,
    }

    template = Template.objects.get(pk=MessageType.WELCOME_USER)
    send_user_email(user, template, email_data, send_html=True)
