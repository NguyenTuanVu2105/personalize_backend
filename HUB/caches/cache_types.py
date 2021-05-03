from django.core.cache import cache, caches

default_cache = cache
redis_cache = caches['redis']
