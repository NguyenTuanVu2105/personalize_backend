import logging

from django.db.models import Prefetch

from HUB.caches import cache_instance, redis_cache, cache_object
from abstract_product.constants import ABSTRACT_PRODUCT_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CACHE_TIMEOUT, \
    ABSTRACT_PRODUCT_PRICING_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_MOCKUP_INFO_CACHE_KEY_PREFIX
from abstract_product.models import AbstractProduct, AbstractProductVariant, ProductAttribute, ProductAttributeValue
from abstract_product.serializers import ProductSerializer
from user_product.functions.mockup_preview_data_generator import mockup_preview_data_generator
from .retrieve_product_pricing import retrieve_product_pricing
from ..querysets import abstract_product_queryset

logger = logging.getLogger(__name__)


def cache_an_abstract_product(abstract_product):
    logger.info(abstract_product)
    product_id = abstract_product.id
    cache_instance(cache_type=redis_cache, instance=abstract_product,
                   serializer=ProductSerializer,
                   cache_key_prefix=ABSTRACT_PRODUCT_CACHE_KEY_PREFIX,
                   timeout=ABSTRACT_PRODUCT_CACHE_TIMEOUT)

    cache_object(obj=retrieve_product_pricing(product_id), cache_type=redis_cache,
                 cache_key=ABSTRACT_PRODUCT_PRICING_CACHE_KEY_PREFIX + str(product_id),
                 timeout=ABSTRACT_PRODUCT_CACHE_TIMEOUT)

    cache_object(obj=mockup_preview_data_generator(product_id), cache_type=redis_cache,
                 cache_key=ABSTRACT_PRODUCT_MOCKUP_INFO_CACHE_KEY_PREFIX + str(product_id),
                 timeout=ABSTRACT_PRODUCT_CACHE_TIMEOUT)


def cache_abstract_products(product_id=None):
    base_queryset = AbstractProduct.objects.filter(is_active=True)
    abstract_products_qs = abstract_product_queryset(base_queryset)

    if product_id:
        abstract_product = abstract_products_qs.get(pk=product_id)
        cache_an_abstract_product(abstract_product)

    else:
        for abstract_product in abstract_products_qs:
            cache_an_abstract_product(abstract_product)

    return True
