import logging
from collections import defaultdict

from service_communication.constants.webhook_job_limits import NUMBER_OF_WEBHOOK_JOB_PER_SCHEDULE_RUN
from service_communication.constants.webhook_job_statuses import WebhookJobStatus
from service_communication.models import WebhookJob
from service_communication.services import WebhookJobService

logger = logging.getLogger(__name__)


def auto_run_all_pending_webhook_job():
    pending_webhook_jobs = WebhookJob.objects.pending().no_delay().only("id", "queue_id")
    jobs_grouped_by_queue_id = defaultdict(list)
    for job in pending_webhook_jobs:
        jobs_grouped_by_queue_id[job.queue_id].append(job.id)
    for queue_id, job_ids in jobs_grouped_by_queue_id.items():
        job_ids = job_ids[:NUMBER_OF_WEBHOOK_JOB_PER_SCHEDULE_RUN]
        WebhookJobService.enqueue_batch_job(queue_id, job_ids)
        WebhookJob.objects.filter(id__in=job_ids).update(status=WebhookJobStatus.QUEUED)
