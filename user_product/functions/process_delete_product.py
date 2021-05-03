from celery.decorators import task

from HUB import CeleryTask
from user_product.functions.sync_product_in_shop.sync_tasks import delete_user_product_in_shop

import logging

logger = logging.getLogger(__name__)


@task(name=CeleryTask.TASK_DELETE_USER_PRODUCT_IN_MULTIPLE_SHOP)
def process_delete_product(shop_user_product_sync_ids):
    for shop_user_product_id in shop_user_product_sync_ids:
        delete_user_product_in_shop.delay(shop_user_product_id)
