from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from user.functions import send_forgot_password_email

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_SEND_FORGOT_PASSWORD_MAIL)
def send_forgot_password_task(user_id, user_email):
    """sends request to send forgot password task"""
    logger.info("send_forgot_password_task")
    return send_forgot_password_email(user_id, user_email)
