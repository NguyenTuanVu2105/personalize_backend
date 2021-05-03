import logging

from HUB.caches import get_cached_object
from abstract_product.constants import ABSTRACT_PRODUCT_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CACHE_TIMEOUT
from abstract_product.querysets import abstract_product_queryset
from abstract_product.serializers import ProductSerializer
from abstract_product.tasks import cache_object_if_not_exist_task

logger = logging.getLogger(__name__)


def retrieve_abstract_product(product_id, base_queryset):
    cache_key = ABSTRACT_PRODUCT_CACHE_KEY_PREFIX + str(product_id)
    cached_object = get_cached_object(cache_key)

    if cached_object:
        response_data = cached_object
    else:
        queryset = abstract_product_queryset(base_queryset)
        product = queryset.get(pk=product_id)
        response_data = ProductSerializer(product).data
        cache_object_if_not_exist_task.delay(cache_key, response_data, ABSTRACT_PRODUCT_CACHE_TIMEOUT)

    return response_data
