class IncomingWebhookStatus:
    PENDING = "0"
    RESOLVED = "1"
    ERROR = "2"
    CANCELLED = "3"


class VerboseIncomingWebhookStatus:
    PENDING = "pending"
    RESOLVED = "resolved"
    ERROR = "error"
    CANCELLED = "cancelled"


INCOMING_WEBHOOK_STATUS_CHOICES = [
    (IncomingWebhookStatus.PENDING, VerboseIncomingWebhookStatus.PENDING),
    (IncomingWebhookStatus.RESOLVED, VerboseIncomingWebhookStatus.RESOLVED),
    (IncomingWebhookStatus.ERROR, VerboseIncomingWebhookStatus.ERROR),
    (IncomingWebhookStatus.CANCELLED, VerboseIncomingWebhookStatus.CANCELLED),
]
