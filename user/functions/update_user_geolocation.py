from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from HUB.functions import get_client_country_code

User = get_user_model()


logger = get_task_logger(__name__)

def update_user_geolocation(user_id, ip_address):
    try:
        user = User.objects.get(id=user_id)
        user.client_ip = ip_address
        user.country_code = get_client_country_code(ip_address)
        user.save()
    except Exception as e:
        logger.info(e)
