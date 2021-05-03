from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from user_product.functions import create_user_variant_prices_by_shop

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_CREATE_USER_VARIANT_PRICES)
def create_user_variant_prices_task(user_id, shop_currency):
    """create user variant prices task"""
    logger.info("Create user variant prices task!!!")
    return create_user_variant_prices_by_shop(user_id, shop_currency)
