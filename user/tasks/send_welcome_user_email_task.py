from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from user.functions.send_welcome_user_email import send_welcome_user_email

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_SEND_WELCOME_USER_EMAIL)
def send_welcome_user_email_task(user_id):
    """sends request to send activation email task"""
    logger.info("send_welcome_user_task")
    return send_welcome_user_email(user_id)
