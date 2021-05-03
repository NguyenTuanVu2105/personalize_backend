from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from ..functions import cache_abstract_category_products

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_CACHE_ABSTRACT_CATEGORY_PRODUCTS)
def cache_abstract_category_products_task():
    return cache_abstract_category_products()
