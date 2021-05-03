import json
import logging
import os

from redis import Redis
from rediscluster import RedisCluster

logger = logging.getLogger(__name__)

REDIS_NODES = json.loads(os.environ.get("REDIS_NODES"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
USE_REDIS_CLUSTER = True if os.environ.get("USE_REDIS_CLUSTER") == "TRUE" else False


def redis_connection():
    try:
        if USE_REDIS_CLUSTER:
            redis = RedisCluster(startup_nodes=REDIS_NODES, decode_responses=True, password=REDIS_PASSWORD)
        else:
            redis = Redis(host=REDIS_NODES[0]["host"], port=REDIS_NODES[0]["port"], db=0, password=REDIS_PASSWORD)

        # redis = RedisCluster(startup_nodes=REDIS_NODES, decode_responses=True, password=REDIS_PASSWORD) if USE_REDIS_CLUSTER else Redis(host=REDIS_NODES[0]["host"], port=REDIS_NODES[0]["port"], db=0, password=REDIS_PASSWORD)

        redis.ping()

    except Exception as e:
        logger.error(str(e))
        return False

    else:
        return redis
