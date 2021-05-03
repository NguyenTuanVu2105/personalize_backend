import logging
import traceback
from datetime import timedelta

import requests

from HUB.celery import app
from helper.choice_helpers import find_verbose_type_from_choices
from helper.datetime_helpers import get_current_datetime
from service_communication.constants.webhook_job_queue_ids import WEBHOOK_JOB_QUEUE_IDS_CHOICES
from service_communication.constants.webhook_job_result_types import WebhookJobResultTypes
from service_communication.constants.webhook_job_statuses import WebhookJobStatus
from service_communication.models import WebhookJob, ServiceCommunicationLog
from .webhook_job_callback_service import WebhookJobCallbackService

logger = logging.getLogger(__name__)


class WebhookJobService:
    RETRY_PERIOD_PER_FAILED_JOB_IN_SECOND = 30
    MAX_ATTEMPT_COUNT = 5

    def __init__(self, queue_id):
        self.queue_id = queue_id

    def create_job(self, request_type, relate_object, relate_params, **kwargs):
        WebhookJob.objects.create(request_type=request_type, relate_object=relate_object,
                                  relate_params=relate_params,
                                  queue_id=self.queue_id,
                                  max_attempt_count=WebhookJobService.MAX_ATTEMPT_COUNT, payload=kwargs)

    @classmethod
    def enqueue_job(cls, webhook_job_obj):
        queue_name = cls.get_webhook_job_queue_name(webhook_job_obj.queue_id)
        WebhookJobService.run_job.apply_async(args=(webhook_job_obj.id,), queue=queue_name)
        webhook_job_obj.set_status(WebhookJobStatus.QUEUED)

    @classmethod
    def enqueue_batch_job(cls, queue_id, job_ids):
        from celery import group
        queue_name = cls.get_webhook_job_queue_name(queue_id)
        async_jobs = list(map(lambda job_id: WebhookJobService.run_job.s(job_id), job_ids))
        group(async_jobs).apply_async(queue=queue_name)

    @staticmethod
    @app.task
    def run_job(webhook_job_id):
        webhook_job_obj = WebhookJobService.get_queued_job(webhook_job_id)
        if not webhook_job_obj:
            return

        # webhook_job_obj.set_status(WebhookJobStatus.PROCESSING, commit=True)
        payload = webhook_job_obj.payload
        queue_name = WebhookJobService.get_webhook_job_queue_name(webhook_job_obj.queue_id)
        log_obj = ServiceCommunicationLog.objects.create(type=webhook_job_obj.request_type,
                                                         webhook_job_id=webhook_job_id,
                                                         relate_object=webhook_job_obj.relate_object,
                                                         payload=payload.get('json'))
        webhook_job_result_type = WebhookJobResultTypes.RETRYABLE
        res = None
        try:
            logger.info("REQUEST WEBHOOK JOB ID-{}".format(webhook_job_obj.id))
            res = requests.request(**payload, timeout=300)
            res.raise_for_status()
        except requests.exceptions.HTTPError:
            status_code = res.status_code
            if status_code in (401, 403):
                webhook_job_result_type = WebhookJobResultTypes.ABORTED
            else:
                webhook_job_result_type = WebhookJobResultTypes.RETRYABLE

            log_obj.response_body = res.text
            log_obj.status_code = status_code
            log_obj.save()
            logger.warning(
                "Error while run webhook job {} - Communication log {} - Http Error [Response status {}]".format(
                    webhook_job_id, log_obj.id, log_obj.status_code))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            webhook_job_result_type = WebhookJobResultTypes.RETRYABLE
            log_obj.response_body = str(e)
            log_obj.status_code = -1
            log_obj.save()
            logger.warning(
                "Error while run webhook job {} - Communication log {} - Connection Error".format(webhook_job_id,
                                                                                                  log_obj.id,
                                                                                                  log_obj.status_code))
        except Exception as e:
            webhook_job_result_type = WebhookJobResultTypes.ABORTED
            error_trace = traceback.format_exc()
            log_obj.response_body = error_trace
            log_obj.status_code = -1
            log_obj.save()
            logger.warning(
                "Error while run webhook job {} - Communication log {} - Unknown Error".format(webhook_job_id,
                                                                                               log_obj.id,
                                                                                               log_obj.status_code))
        else:
            webhook_job_result_type = WebhookJobResultTypes.SUCCEED
            log_obj.response_body = res.text
            log_obj.status_code = res.status_code
            log_obj.response_time = get_current_datetime()
            log_obj.save()
            logger.info("Succeeded to run webhook job {} - Communication log {} - Response status: {}".format(
                webhook_job_id, log_obj.id, log_obj.status_code))
        WebhookJobService.handle_job_result(webhook_job_id, queue_name, webhook_job_result_type,
                                            res.text if res else None)

    @staticmethod
    def handle_job_result(webhook_job_id, queue_name, webhook_job_result_type, response_text):
        webhook_job_obj = WebhookJobService.get_queued_job(webhook_job_id)
        if not webhook_job_obj:
            return
        webhook_job_obj.attempted_count += 1
        if webhook_job_result_type == WebhookJobResultTypes.SUCCEED:
            webhook_job_obj.set_status(WebhookJobStatus.SUCCESS)
            try:
                WebhookJobCallbackService.handle_successful_result(webhook_job_obj, response_text)
            except Exception as e:
                logger.exception(e)
            else:
                # if handle_successful_result had no exception
                # -> return immediately
                # else continue to handle as error case
                return

        if webhook_job_result_type == WebhookJobResultTypes.RETRYABLE and webhook_job_obj.should_retry:
            next_run_countdown = WebhookJobService.RETRY_PERIOD_PER_FAILED_JOB_IN_SECOND * webhook_job_obj.attempted_count ** 2
            next_run_time = get_current_datetime() + timedelta(seconds=next_run_countdown)
            webhook_job_obj.set_next_run_time(next_run_time, commit=False)
            webhook_job_obj.set_status(WebhookJobStatus.PENDING, commit=True)
            logger.info("Scheduled to retry webhook job {} after {}".format(webhook_job_id, next_run_countdown))
        else:
            webhook_job_obj.set_status(WebhookJobStatus.FAILED)
            WebhookJobCallbackService.handle_failed_result(webhook_job_obj, response_text)

    @staticmethod
    def stop_job(webhook_job_id):
        webhook_job_obj = WebhookJobService.get_cancelable_job(webhook_job_id)
        assert webhook_job_obj, 'Invalid webhook_job_id'
        webhook_job_obj.set_status(WebhookJobStatus.FAILED)
        WebhookJobCallbackService.handle_failed_result(webhook_job_obj, None)

    @staticmethod
    def get_queued_job(webhook_job_id):
        webhook_job_obj = WebhookJob.objects.queued().filter(id=webhook_job_id).first()
        return webhook_job_obj

    @staticmethod
    def get_cancelable_job(webhook_job_id):
        webhook_job_obj = WebhookJob.objects.cancelable_filter().filter(id=webhook_job_id).first()
        return webhook_job_obj

    @staticmethod
    def get_webhook_job_queue_name(webhook_job_queue_id):
        return find_verbose_type_from_choices(WEBHOOK_JOB_QUEUE_IDS_CHOICES, webhook_job_queue_id)
