from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from user.functions.bulk_resync_product import bulk_resync_product

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_BULK_RESYNC_PRODUCT)
def bulk_resync_product_task(user_product_id, shop_ids):
    """sends request to bulk resync product task"""
    logger.info("bulk_resync_product_task")
    return bulk_resync_product(user_product_id, shop_ids)
