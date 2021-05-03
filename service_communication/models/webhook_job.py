from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import timezone

from HUB.models.random_id_model import RandomIDModel
from helper.choice_helpers import find_verbose_type_from_choices
from service_communication.constants.request_type import REQUEST_TYPES
from service_communication.constants.webhook_job_queue_ids import WEBHOOK_JOB_QUEUE_IDS_CHOICES
from service_communication.constants.webhook_job_statuses import WEBHOOK_JOB_STATUS_CHOICES, WebhookJobStatus
from service_communication.managers.webhook_job_manager import WebhookJobManager


def get_verbose_request_type(request_type):
    return find_verbose_type_from_choices(REQUEST_TYPES, request_type)


def get_verbose_status(status):
    return find_verbose_type_from_choices(WEBHOOK_JOB_STATUS_CHOICES, status)


class WebhookJob(RandomIDModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    queue_id = models.CharField(max_length=2, choices=WEBHOOK_JOB_QUEUE_IDS_CHOICES, db_index=True)
    next_run_time = models.DateTimeField(default=timezone.now)
    object_id = models.BigIntegerField()
    relate_object = GenericForeignKey('content_type', 'object_id')
    request_type = models.CharField(max_length=2, choices=REQUEST_TYPES, db_index=True)
    status = models.CharField(max_length=2, choices=WEBHOOK_JOB_STATUS_CHOICES, default=WebhookJobStatus.PENDING,
                              db_index=True)
    relate_params = JSONField(blank=True, default=dict, encoder=DjangoJSONEncoder)
    payload = JSONField(encoder=DjangoJSONEncoder)
    attempted_count = models.IntegerField(default=0, blank=True)
    max_attempt_count = models.IntegerField(default=-1, blank=True)
    is_aborted = models.BooleanField(blank=True, default=False, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    tsv_metadata_search = SearchVectorField(null=True)

    objects = WebhookJobManager()

    class Meta:
        ordering = ['-id']
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    @property
    def verbose_request_type(self):
        return get_verbose_request_type(self.request_type)

    @property
    def verbose_status(self):
        return get_verbose_status(self.status)

    @property
    def should_retry(self):
        return self.max_attempt_count < 0 or self.attempted_count < self.max_attempt_count

    def set_next_run_time(self, next_run_time, commit=True):
        self.next_run_time = next_run_time
        if commit:
            self.save()

    def set_status(self, new_status, commit=True):
        if not self.is_failed:
            self.status = new_status
            if commit:
                self.save()

    @property
    def is_recoverable(self):
        return not self.is_aborted and self.is_failed and self.relate_params != {}

    @property
    def is_cancellable(self):
        return self.status == WebhookJobStatus.PENDING or WebhookJobStatus.QUEUED

    @property
    def is_failed(self):
        return self.status == WebhookJobStatus.FAILED

    def set_aborted(self):
        self.is_aborted = True
        self.save()
