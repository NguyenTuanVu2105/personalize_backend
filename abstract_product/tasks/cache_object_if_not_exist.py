from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.caches import redis_cache, cache_object
from HUB.constants.celery_task import CeleryTask

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_CACHE_OBJECT_IF_NOT_EXIST)
def cache_object_if_not_exist_task(cache_key, cache_data, timeout, cache_type=redis_cache):
    return cache_object(cache_type=cache_type, cache_key=cache_key, obj=cache_data, timeout=timeout)
