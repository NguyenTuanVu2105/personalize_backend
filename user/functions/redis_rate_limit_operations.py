from user.functions import redis_connection
from user.functions.rate_limit import DEFAULT_RATE_LIMIT_REDIS_TIMEOUT


def get_rate_limit(key, empty_key_value=None):
    redis = redis_connection()
    if redis:
        rate_limit = redis.get(key)
        # redis.expire(key, time=DEFAULT_RATE_LIMIT_REDIS_TIMEOUT)
        return rate_limit
    return None


def set_rate_limit(key, limit):
    redis = redis_connection()
    if redis and limit:
        redis.setnx(key, limit)
        redis.expire(key, time=DEFAULT_RATE_LIMIT_REDIS_TIMEOUT)
        return limit
    return None
