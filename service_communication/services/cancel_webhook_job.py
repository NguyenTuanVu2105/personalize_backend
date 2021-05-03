import traceback

from service_communication.services import WebhookJobService


def bulk_cancel_webhook_job(job_ids):
    for job_id in job_ids:
        success = cancel_webhook_job(job_id)
        if success:
            continue
        else:
            return False

    return True


def cancel_webhook_job(job_id):
    success = False
    try:
        WebhookJobService.stop_job(job_id)
    except AssertionError as e:
        pass
    except Exception as e:
        traceback.print_tb(e.__traceback__)
    else:
        success = True
    return success
