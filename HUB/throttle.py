import logging

from rest_framework import throttling

from HUB.caches import redis_cache, default_cache
from user.contants.rate_limit_views import RateLimitView
from user.functions import check_rate_limit
from django.conf import settings
logger = logging.getLogger(__name__)


class UserThrottle(throttling.BaseThrottle):
    scope_attr = 'throttle_view'

    def allow_request(self, request, view):
        if not request.user.is_authenticated:
            return False
        view = getattr(view, self.scope_attr, RateLimitView.CREATE_USER_PRODUCT)

        # Check deny cache, True = in cache => deny this request without check DB
        cache_key = f'request_limited_{view}_{request.user.id}'

        if redis_cache.get(cache_key, False) or default_cache.get(cache_key, False):
            return False

        allowed = check_rate_limit(view=view, user_id=request.user.id)
        if not allowed:
            redis_cache.set(cache_key, True, settings.DEFAULT_RATE_LIMIT_PERIOD * 60)
            default_cache.set(cache_key, True, settings.DEFAULT_RATE_LIMIT_PERIOD * 60)

        return allowed

