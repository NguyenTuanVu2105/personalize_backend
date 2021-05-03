from rest_framework.response import Response

from HUB.caches import redis_cache
from HUB.views import AdminAPIView
from abstract_product.constants import ABSTRACT_PRODUCT_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX, \
    ABSTRACT_PRODUCT_MOCKUP_INFO_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_PRICING_CACHE_KEY_PREFIX

class AdminCache(AdminAPIView):
    deletable_prefix = list(
        map(lambda s: s.strip('_'), [ABSTRACT_PRODUCT_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX,
                                     ABSTRACT_PRODUCT_MOCKUP_INFO_CACHE_KEY_PREFIX,
                                     ABSTRACT_PRODUCT_PRICING_CACHE_KEY_PREFIX]))

    ALL_KEY_PREFIX = 'all'

    def delete(self, request, prefix=''):
        if prefix == self.ALL_KEY_PREFIX:
            redis_cache.clear()
        elif prefix in self.deletable_prefix:
            redis_cache.delete_pattern(pattern=prefix + '_*')
        return Response({'success': True})

    def get(self, request, prefix=''):
        return Response({'data': str(redis_cache.keys(prefix + '*'))})
