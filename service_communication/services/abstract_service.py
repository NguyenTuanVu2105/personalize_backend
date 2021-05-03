import logging
import traceback

import requests
from django.utils import timezone

from service_communication.models import ServiceCommunicationLog
from .webhook_job_services import WebhookJobService

logger = logging.getLogger(__name__)


class AbstractCommunicationService:
    webhook_job_service = WebhookJobService(queue_id=None)

    @classmethod
    def create_request_job(cls, request_type, relate_object, relate_params, method, url, data, headers):
        cls.webhook_job_service.create_job(request_type=request_type, relate_object=relate_object,
                                           relate_params=relate_params, method=method, url=url,
                                           json=data, headers=headers)

    @classmethod
    def request_and_log(cls, request_type, request_object, method, url, data, headers):
        service_log = ServiceCommunicationLog.objects.create(type=request_type,
                                                             relate_object=request_object,
                                                             request_time=timezone.now(),
                                                             payload=data)
        try:
            res = requests.request(method, url, json=data, headers=headers)
            # logger.info(res.text)
            service_log.response_body = res.text
            service_log.status_code = res.status_code
            service_log.response_time = timezone.now()
            service_log.save()
            return res
        except Exception as e:
            error_trace = traceback.format_exc()
            service_log.response_body = error_trace
            service_log.status_code = -1
            service_log.save()
            raise e
