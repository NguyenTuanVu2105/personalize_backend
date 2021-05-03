from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from user.functions import update_user_geolocation

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_UPDATE_USER_GEOLOCATION)
def update_geolocation_task(user_id, ip_address):
    """update user ip address and country code"""
    logger.info("update_user_geolocation")
    return update_user_geolocation(user_id, ip_address)
