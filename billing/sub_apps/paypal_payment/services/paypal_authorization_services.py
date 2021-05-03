import logging
from celery.decorators import task
from datetime import timedelta

import requests
from requests.auth import HTTPBasicAuth

from HUB import settings
from helper.datetime_helpers import get_current_datetime
from service_communication.constants.schedule_type import ScheduleType
from service_communication.models import ScheduleInfo
from .paypal_endpoint_service import PaypalEndpointService
from HUB.constants.celery_task import CeleryTask

PRODUCT_VENDOR_NAME = settings.PRODUCT_VENDOR_NAME or ""

logger = logging.getLogger(__name__)


class PaypalAuthorizationService:
    API_V1 = settings.PAYPAL_APP_API_V1
    CLIENT_ID = settings.PAYPAL_APP_CLIENT_ID
    SECRET_KEY = settings.PAYPAL_APP_SECRET_KEY

    ACCESS_TOKEN = None
    EXPIRATION = get_current_datetime()

    @classmethod
    def _renew_access_token_from_paypal(cls, ignore_cache=True):
        try:
            response = requests.post(url=PaypalEndpointService.GET_ACCESS_TOKEN_ENDPOINT,
                                     auth=HTTPBasicAuth(cls.CLIENT_ID, cls.SECRET_KEY),
                                     data={"grant_type": "client_credentials",
                                           "ignoreCache": str(ignore_cache).lower()})
            response.raise_for_status()
        except Exception as e:
            logger.error("Can't get paypal access token")
            logger.exception(e)
        else:
            return response.json()

    @classmethod
    def renew_access_token_from_db(cls, force=False):
        paypal_token_schedule_obj = ScheduleInfo.objects.filter(
            schedule_type=ScheduleType.AUTO_RENEW_PAYPAL_TOKEN).first()

        if not force and paypal_token_schedule_obj:
            meta_data = paypal_token_schedule_obj.meta
            expires_in = meta_data.get("expires_in")
            if expires_in and isinstance(expires_in, int):
                current_time = get_current_datetime()
                if paypal_token_schedule_obj.update_time + timedelta(seconds=expires_in - 3600) > current_time:
                    return

        # avoid to get access token multiple times after expired so just keep it cached from paypal
        ignore_cache = not force

        response_json = PaypalAuthorizationService._renew_access_token_from_paypal(ignore_cache=ignore_cache)
        ScheduleInfo.objects.update_or_create(schedule_type=ScheduleType.AUTO_RENEW_PAYPAL_TOKEN,
                                              defaults={"meta": response_json})

    @staticmethod
    @task(name=CeleryTask.TASK_RENEW_PAYPAL_ACCESS_TOKEN)
    def _task_auto_renew_db_paypal_token(*args, **kwargs):
        return PaypalAuthorizationService.renew_access_token_from_db(*args, **kwargs)

    @classmethod
    def reset_token_and_renew_from_db(cls):
        cls.ACCESS_TOKEN = None
        cls._task_auto_renew_db_paypal_token.delay(force=True)

    @classmethod
    def _reload_access_token_from_db(cls):
        paypal_token_schedule_obj = ScheduleInfo.objects.filter(
            schedule_type=ScheduleType.AUTO_RENEW_PAYPAL_TOKEN).first()
        if paypal_token_schedule_obj:
            cls.EXPIRATION = get_current_datetime() + timedelta(seconds=900)
            cls.ACCESS_TOKEN = paypal_token_schedule_obj.meta["access_token"]

    @classmethod
    def get_access_token(cls):
        current_time = get_current_datetime()
        if not cls.ACCESS_TOKEN or current_time > cls.EXPIRATION:
            cls._reload_access_token_from_db()
        return cls.ACCESS_TOKEN

    @classmethod
    def get_client_id(cls):
        return cls.CLIENT_ID
