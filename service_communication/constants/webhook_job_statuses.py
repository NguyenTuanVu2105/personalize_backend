class WebhookJobStatus:
    SUCCESS = '1'
    PENDING = '2'
    FAILED = '3'
    QUEUED = '4'
    PROCESSING = '5'


class VerboseWebhookJobStatus:
    SUCCESS = 'success'
    PENDING = 'pending'
    FAILED = 'failed'
    QUEUED = 'queued'
    PROCESSING = 'processing'


WEBHOOK_JOB_STATUS_CHOICES = [
    (WebhookJobStatus.SUCCESS, VerboseWebhookJobStatus.SUCCESS),
    (WebhookJobStatus.PENDING, VerboseWebhookJobStatus.PENDING),
    (WebhookJobStatus.FAILED, VerboseWebhookJobStatus.FAILED),
    (WebhookJobStatus.QUEUED, VerboseWebhookJobStatus.QUEUED),
    (WebhookJobStatus.PROCESSING, VerboseWebhookJobStatus.PROCESSING)
]
