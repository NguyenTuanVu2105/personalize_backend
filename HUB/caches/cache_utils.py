import json
import zlib

from HUB.caches import redis_cache


def cache_object(obj, cache_key, timeout, cache_type=redis_cache, compress=True):
    cache_value = obj
    if compress:
        cache_value = zlib.compress(json.dumps(obj, separators=(',', ':')).encode('utf-8'), 9)
    cache_type.set(key=cache_key, value=cache_value, timeout=timeout)


def cache_instance(cache_type, instance, serializer, cache_key_prefix='', timeout=None):
    serialized_object = serializer(instance=instance).data
    cache_key = cache_key_prefix + str(instance.id)
    cache_object(serialized_object, cache_key, timeout, cache_type)
    return serialized_object


def get_cached_object(cache_key, cache_type=redis_cache, decompress=True):
    cached_object = cache_type.get(cache_key)
    if cached_object and decompress:
        return json.loads(zlib.decompress(cached_object), encoding='utf-8')
    return cached_object


def delete_cached_object(cache_key, cache_type=redis_cache):
    cache_type.delete(cache_key)
