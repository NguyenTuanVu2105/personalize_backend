from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from service_communication.constants.request_type import REQUEST_TYPES, RequestType
from .webhook_job import WebhookJob


class ServiceCommunicationLog(RandomIDModel):
    type = models.CharField(max_length=2, choices=REQUEST_TYPES,
                            default=RequestType.FULFILL_PUSH_ORDER, blank=True, db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.BigIntegerField(null=True, blank=True)
    relate_object = GenericForeignKey('content_type', 'object_id')
    webhook_job = models.ForeignKey(to=WebhookJob, on_delete=models.SET_NULL, related_name="communication_logs",
                                    null=True, blank=True)
    status_code = models.IntegerField(null=True)
    response_body = models.TextField()
    request_time = models.DateTimeField(auto_now_add=True)
    response_time = models.DateTimeField(auto_now_add=True)
    payload = JSONField(default=dict)

    tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = 'service_communication_log'
        ordering = ['-id']
        indexes = [GinIndex(fields=["tsv_metadata_search"])]
