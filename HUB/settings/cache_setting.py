import json
import os

USE_REDIS_CLUSTER = True if os.environ.get("USE_REDIS_CLUSTER") == "TRUE" else False
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
if USE_REDIS_CLUSTER:
    REDIS_OPTIONS = {
        "PASSWORD": REDIS_PASSWORD,
        'REDIS_CLIENT_CLASS': 'rediscluster.RedisCluster',
        'CONNECTION_POOL_CLASS': 'rediscluster.connection.ClusterConnectionPool',
        'CONNECTION_POOL_KWARGS': {
            'skip_full_coverage_check': True
        },
        'IGNORE_EXCEPTIONS': True
    }
    REDIS_LOCATION = [f'redis://:{REDIS_PASSWORD}@{node["host"]}:{node["port"]}/0' for node in
                      json.loads(os.environ.get("REDIS_NODES"))]
else:
    REDIS_OPTIONS = {
        "PASSWORD": REDIS_PASSWORD,
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
        "IGNORE_EXCEPTIONS": True
    }
    REDIS_LOCATION = [f'redis://{node["host"]}:{node["port"]}/0' for node in json.loads(os.environ.get("REDIS_NODES"))]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    },
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": REDIS_OPTIONS
    }
}

DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
# DJANGO_REDIS_LOGGER = __name__
