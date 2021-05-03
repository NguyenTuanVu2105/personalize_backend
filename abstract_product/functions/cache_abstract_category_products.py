import logging

from HUB.caches import cache_instance, redis_cache
from abstract_product.constants import ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CACHE_TIMEOUT
from abstract_product.models import AbstractProductCategory
from abstract_product.serializers import AbstractProductCategorySerializer
from ..querysets import abstract_product_category_queryset

logger = logging.getLogger(__name__)


def cache_abstract_category_products():
    base_queryset = AbstractProductCategory.objects.filter(is_active=True).exclude(title="Popular").order_by(
        '-force_active', '-sort_index')
    abstract_categories = abstract_product_category_queryset(base_queryset=base_queryset)

    if abstract_categories:
        for abstract_category in abstract_categories:
            cache_instance(cache_type=redis_cache, instance=abstract_category,
                           serializer=AbstractProductCategorySerializer,
                           cache_key_prefix=ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX,
                           timeout=ABSTRACT_PRODUCT_CACHE_TIMEOUT)

        return True

    return False
