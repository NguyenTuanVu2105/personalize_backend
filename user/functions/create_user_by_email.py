import logging

from django.contrib.auth import get_user_model

from HUB.helpers.randox_hex import random_hex
from notification.services.instant_prompt import generate_default_instant_prompt
from shop.functions import create_user_printholo_store
from user.functions.send_activation_email import send_activation_email
from user.functions.send_created_account_email import send_created_account_email

User = get_user_model()
logger = logging.getLogger(__name__)


def create_user_by_email(email, email_source, user_name, address, phone):
    password = random_hex(16)
    user = User.objects.create(email=email, name=user_name, account_type=email_source, address=address,
                               phone_number=phone)
    user.set_password(password)
    user.save()

    # logger.info("USER ID 1")
    # logger.info(user.id)
    # logger.info(user.id)

    generate_default_instant_prompt(user.id)
    send_created_account_email(user_id=user.id, password=password)
    create_user_printholo_store(user=user)
    send_activation_email(user_id=user.id)

    # if created:
    #     generate_default_instant_prompt(user.id)
    #     send_created_account_email_task.delay(user_id=user.id, password=password)
    #     send_activation_email_task.delay(user_id=user.id)
    #     create_user_printholo_store(user=user)

    return user
