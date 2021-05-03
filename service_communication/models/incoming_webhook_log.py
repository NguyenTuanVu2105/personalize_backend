from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from helper.choice_helpers import find_verbose_type_from_choices
from service_communication.constants.incoming_webhook_statuses import INCOMING_WEBHOOK_STATUS_CHOICES, IncomingWebhookStatus
from service_communication.constants.incoming_webhook_types import INCOMING_WEBHOOK_TYPE_CHOICES, IncomingWebhookType


class IncomingWebhook(RandomIDModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.BigIntegerField(null=True, blank=True)
    relate_object = GenericForeignKey('content_type', 'object_id')
    type = models.CharField(max_length=2, choices=INCOMING_WEBHOOK_TYPE_CHOICES, default=IncomingWebhookType.FULFILL_PROCESS_ORDER, db_index=True)
    body_data = JSONField(null=True, blank=True)
    meta = JSONField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=INCOMING_WEBHOOK_STATUS_CHOICES, default=IncomingWebhookStatus.PENDING, db_index=True)
    process_description = models.CharField(max_length=255, null=True, blank=True)
    process_count = models.SmallIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = "service_communication_incoming_webhook"
        ordering = ["-update_time"]
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    @property
    def verbose_type(self):
        return find_verbose_type_from_choices(INCOMING_WEBHOOK_TYPE_CHOICES, self.type)

    @property
    def verbose_status(self):
        return find_verbose_type_from_choices(INCOMING_WEBHOOK_STATUS_CHOICES, self.status)
