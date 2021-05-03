from user.functions import redis_connection


def get_redis_num_unread_msg_key(user):
    return f'{user.id}_num_unread_msg'


def get_num_unread_msg(user):
    try:
        redis = redis_connection()
        return int(redis.get(get_redis_num_unread_msg_key(user)))
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(e)
        return None


def set_num_unread_msg(user, num_unread_msg):
    try:
        redis = redis_connection()
        return redis.set(get_redis_num_unread_msg_key(user), num_unread_msg)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(e)
        return None
