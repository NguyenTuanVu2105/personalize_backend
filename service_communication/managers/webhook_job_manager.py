from django.db.models import QuerySet, Manager

from helper.datetime_helpers import get_current_datetime
from service_communication.constants.webhook_job_statuses import WebhookJobStatus


class WebhookJobQueryset(QuerySet):
    def pending(self):
        return self.filter(status=WebhookJobStatus.PENDING)

    def queued(self):
        return self.filter(status=WebhookJobStatus.QUEUED)

    def processing(self):
        return self.filter(status=WebhookJobStatus.PROCESSING)

    def cancelable_filter(self):
        return self.filter(status__in=[WebhookJobStatus.QUEUED, WebhookJobStatus.PENDING])

    def no_delay(self):
        current_time = get_current_datetime()
        return self.filter(next_run_time__lte=current_time)


WebhookJobManager = Manager.from_queryset(WebhookJobQueryset)
