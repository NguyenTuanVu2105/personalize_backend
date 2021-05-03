from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from support.constants.ticket_statuses import SUPPORT_TICKET_STATUSES, SupportTicketStatus, SUPPORT_TICKET_STATUS_DICT
from support.constants.ticket_types import SUPPORT_TICKET_TYPES, SupportTicketType
from user.models import User


class SupportTicket(RandomIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ticket_id = models.BigIntegerField(db_index=True)
    url = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=SUPPORT_TICKET_TYPES, default=SupportTicketType.ORDER)
    status = models.CharField(max_length=1, choices=SUPPORT_TICKET_STATUSES, default=SupportTicketStatus.OPEN)
    description = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    last_reply = models.DateTimeField(null=True, blank=True)
    need_update = models.BooleanField(default=False)
    attachments = ArrayField(JSONField(null=True, blank=True), blank=True, null=True, default=[])
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(db_index=True)
    read = models.BooleanField(default=True)
    customer_last_reply = models.BooleanField(null=True, blank=True)
    tsv_metadata_search = SearchVectorField(null=True)

    @property
    def verbose_status(self):
        return SUPPORT_TICKET_STATUS_DICT.get(self.status)

    @property
    def is_resolved(self):
        return self.status in [SupportTicketStatus.RESOLVED, SupportTicketStatus.CLOSED]

    class Meta:
        db_table = 'support_ticket'
        ordering = ["-create_time"]
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

