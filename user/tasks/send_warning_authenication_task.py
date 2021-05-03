from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from user.functions.send_warning_authenication import send_warning_authenication

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_SEND_WARNING_AUTHENICATION)
def send_warning_authenication_task(user_id):
    """sends request to send activation email task"""
    logger.info("send_warning_authenication_task")
    return send_warning_authenication(user_id)
