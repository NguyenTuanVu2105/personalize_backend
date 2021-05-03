from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from user.functions.send_created_account_email import send_created_account_email

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_SEND_CREATED_ACCOUNT_EMAIL)
def send_created_account_email_task(user_id, password):
    """sends created account email task"""
    logger.info("send_created_account_email_task")
    return send_created_account_email(user_id, password)
