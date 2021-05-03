import logging

from service_communication.models import WebhookJob

logger = logging.getLogger(__name__)


class WebhookJobRecoveryService:
    """
        Use to recover (reinitialize) new webhook job from old failed webhook job.
        New webhook job payload will be built based on old failed webhook job's relate object IDs and relate function registered to recovery service
    """

    WEBHOOK_JOB_RECOVERY_FUNCTIONS = {
        # FORMAT: request_type : relate_function
    }

    @classmethod
    def register_function(cls, request_type, function):
        assert request_type not in cls.WEBHOOK_JOB_RECOVERY_FUNCTIONS, "Duplicate request_type {} function while registering to webhook job recovery service".format(
            request_type)
        assert callable(function), "Invalid function registered, a callable object is required"
        cls.WEBHOOK_JOB_RECOVERY_FUNCTIONS[request_type] = function

    @classmethod
    def get_job(cls, webhook_job_id):
        webhook_job = WebhookJob.objects.filter(id=webhook_job_id).first()
        assert webhook_job and webhook_job.is_recoverable, "Webhook Job ID is invalid"
        return webhook_job

    @classmethod
    def recover_job(cls, webhook_job_id):
        webhook_job = cls.get_job(webhook_job_id)
        if webhook_job:
            webhook_job.set_aborted()
            cls.call_relate_function(webhook_job.request_type, webhook_job.relate_params)

    @classmethod
    def call_relate_function(cls, request_type, params):
        try:
            cls.WEBHOOK_JOB_RECOVERY_FUNCTIONS.get(request_type)(**params)
        except KeyError:
            logger.warning(
                "Function with request_type {} is not registered to webhook job recovery service".format(request_type))
