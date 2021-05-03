import logging

from user.models import UserLimit, UserRateLimitDefault

logger = logging.getLogger(__name__)


def retrieve_max_allow_rate_limit(view, user_id):
    # logger.info("Retrieving rate limit for user {} | view {} ...".format(user_id, view))
    try:
        user_rate_limit_object = UserLimit.objects.only('rate_limit').get(user_id=user_id, view=view)
    except UserLimit.DoesNotExist:
        # logger.info("UserLimit does not exist. Retrieving UserRateLimitDefault instead ...")
        try:
            user_rate_limit_object = UserRateLimitDefault.objects.only('rate_limit').get(view=view)
        except UserRateLimitDefault.DoesNotExist:
            # logger.info("UserRateLimitDefault also does not exist. Using 100 as a default rate limit ...")
            return 100
        else:
            return user_rate_limit_object.rate_limit
    else:
        return user_rate_limit_object.rate_limit
