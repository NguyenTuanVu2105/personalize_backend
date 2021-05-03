import logging
import os

from django.contrib.auth import get_user_model

from notification.enums.message_types import MessageType
from notification.models import Template
from notification.services.notification import send_user_email

User = get_user_model()

PROFILE_LINK_FORMAT = "{0}/u/profile"

logger = logging.getLogger(__name__)


def send_created_account_email(user_id, password):
    # logger.info("USER ID 2")
    # logger.info(user_id)
    # logger.info(user_id)
    user = User.objects.get(id=user_id)
    client_site = os.environ.get("CLIENT_URL")
    # query_params = "email={}"

    profile_link = PROFILE_LINK_FORMAT.format(client_site)
    email_data = {
        "email": user.email,
        "password": password,
        "profile_link": profile_link
    }

    template = Template.objects.get(pk=MessageType.CREATE_ACCOUNT_BY_EMAIL)
    send_user_email(user, template, email_data, send_html=True)
