from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from ..functions import cache_abstract_products

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_CACHE_ABSTRACT_PRODUCT)
def cache_abstract_products_task(product_id=None):
    return cache_abstract_products(product_id)
