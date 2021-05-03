from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from user.functions.send_activation_email import send_activation_email

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_SEND_ACTIVATION_EMAIL)
def send_activation_email_task(user_id):
    """sends request to send activation email task"""
    logger.info("send_activation_email_task")
    return send_activation_email(user_id)
