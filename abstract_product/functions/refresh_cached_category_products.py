from abstract_product.constants import ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CACHE_TIMEOUT
from abstract_product.querysets import abstract_product_category_queryset
from abstract_product.serializers import AbstractProductCategorySerializer
from abstract_product.tasks import cache_object_if_not_exist_task
from abstract_product.viewsets import AbstractProductCategoryViewSet


def refresh_cached_category_products():
    base_category_queryset = AbstractProductCategoryViewSet().get_queryset()
    category_queryset = abstract_product_category_queryset(base_category_queryset)
    for category in category_queryset:
        category_id = str(category.id)
        cache_key = ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX + category_id
        response_data = AbstractProductCategorySerializer(category).data
        cache_object_if_not_exist_task.delay(cache_key, response_data, ABSTRACT_PRODUCT_CACHE_TIMEOUT)

    return None
