from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from helper.choice_helpers import find_verbose_type_from_choices
from service_communication.constants.rejected_request_statuses import RejectedRequestStatus, REJECTED_REQUEST_STATUS_CHOICES
from service_communication.constants.request_type import REQUEST_TYPES
from service_communication.models.webhook_job import get_verbose_request_type
from user.models import User


class RejectedRequest(RandomIDModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    relate_object = GenericForeignKey('content_type', 'object_id')
    request_type = models.CharField(max_length=2, choices=REQUEST_TYPES, db_index=True)
    detail = JSONField()
    status = models.CharField(max_length=2, choices=REJECTED_REQUEST_STATUS_CHOICES, default=RejectedRequestStatus.PENDING, db_index=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    last_update_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="process_order_rejected_by_fulfills", null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = "service_communication_rejected_request"
        ordering = ["-update_time"]
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    @property
    def verbose_request_type(self):
        return get_verbose_request_type(self.request_type)

    @property
    def verbose_status(self):
        return find_verbose_type_from_choices(REJECTED_REQUEST_STATUS_CHOICES, self.status)
