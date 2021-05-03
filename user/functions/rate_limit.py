import datetime
import logging

from django.conf import settings

from user.contants import RATE_LIMIT_PREFIX
from .redis_connection import redis_connection
from .retrieve_max_allow_rate_limit import retrieve_max_allow_rate_limit

DEFAULT_RATE_LIMIT = settings.DEFAULT_RATE_LIMIT
DEFAULT_RATE_LIMIT_PERIOD = settings.DEFAULT_RATE_LIMIT_PERIOD  # minutes
DEFAULT_RATE_LIMIT_REDIS_TIMEOUT = DEFAULT_RATE_LIMIT_PERIOD * 60 * 3

logger = logging.getLogger(__name__)


def check_rate_limit(view, user_id):
    redis = redis_connection()

    if redis:
        current = datetime.datetime.now()
        current_in_minute = current.minute
        current_rate_limit_key = "{}{}_{}_{}".format(RATE_LIMIT_PREFIX, view, user_id, current.strftime("%Y%m%d%H"))
        previous_hour = current - datetime.timedelta(hours=1)
        previous_rate_limit_key = "{}{}_{}_{}".format(RATE_LIMIT_PREFIX, view, user_id,
                                                      previous_hour.strftime("%Y%m%d%H"))

        current_rate_limit = redis.get(current_rate_limit_key)
        previous_rate_limit = redis.get(previous_rate_limit_key)

        if not current_rate_limit or not previous_rate_limit:
            user_rate_limit = retrieve_max_allow_rate_limit(view, user_id)
            if not previous_rate_limit:
                redis.set(previous_rate_limit_key, user_rate_limit, ex=DEFAULT_RATE_LIMIT_REDIS_TIMEOUT)
                previous_rate_limit = user_rate_limit
            if not current_rate_limit:
                redis.setnx(current_rate_limit_key, user_rate_limit)
                redis.expire(current_rate_limit_key, time=DEFAULT_RATE_LIMIT_REDIS_TIMEOUT)

        current_remain = redis.decr(current_rate_limit_key)
        previous_remain = previous_rate_limit
        summary_remain = int(
            (1 - current_in_minute / DEFAULT_RATE_LIMIT_PERIOD) * int(previous_remain) + int(current_remain))
        return summary_remain > 0

    else:
        return True
        # cache_key = f'request_limited_{view}_{user_id}'
        # with connection.cursor() as cursor:
        #     cursor.execute(f"SELECT check_rate_limit('{view}', {user_id})")
        #     allowed = cursor.fetchall()[0][0]
        #     if not allowed:
        #         default_cache.set(cache_key, True, settings.DEFAULT_RATE_LIMIT_PERIOD * 60)
        #
        #     return allowed
