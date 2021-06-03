import logging

from celery.decorators import task
from django.contrib.contenttypes.models import ContentType

from HUB.constants.celery_task import CeleryTask
from service_communication.models import ServiceCommunicationLog

logger = logging.getLogger(__name__)


@task(name=CeleryTask.TASK_CREATE_SERVICE_COMMUNICATION_LOG)
def create_service_communication_log_task(request_type,
                                          content_type_id,
                                          object_id,
                                          webhook_job_id,
                                          status_code,
                                          response_body,
                                          request_time,
                                          response_time,
                                          payload):
    ServiceCommunicationLog.objects.create(
        type=request_type,
        content_type_id=content_type_id,
        object_id=object_id,
        webhook_job_id=webhook_job_id,
        status_code=status_code,
        response_body=response_body,
        request_time=request_time,
        response_time=response_time,
        payload=payload
    )


def create_service_communication_log_async(request_type,
                                           status_code,
                                           response_body_as_text,
                                           request_time,
                                           response_time,
                                           related_object=None,
                                           webhook_job=None,
                                           payload=None,
                                           ):
    try:
        if related_object:
            content_type_id = ContentType.objects.get_for_model(related_object).id
            object_id = related_object.id
        else:
            content_type_id = None
            object_id = None
        if webhook_job:
            webhook_job_id = webhook_job.id
        else:
            webhook_job_id = None
        if not payload:
            payload = {}
        create_service_communication_log_task.delay(
            request_type=request_type,
            content_type_id=content_type_id,
            object_id=object_id,
            webhook_job_id=webhook_job_id,
            status_code=status_code,
            response_body=response_body_as_text,
            request_time=request_time,
            response_time=response_time,
            payload=payload
        )
    except Exception as e:
        logger.error(e)


def extract_invoice_id_from_payload(json):
    try:
        request_invoice_id = None
        if 'purchase_units' in json:
            purchase_unit = json['purchase_units'][0]
            if 'invoice_id' in purchase_unit:
                request_invoice_id = purchase_unit['invoice_id']
        elif 'transactions' in json:
            transaction = json['transactions'][0]
            if 'invoice_number' in transaction:
                request_invoice_id = transaction['invoice_number']
        invoice_id = request_invoice_id[request_invoice_id.index('_') + 1:] if request_invoice_id else None
    except Exception as e:
        logger.info(e)
        invoice_id = None
    return invoice_id
