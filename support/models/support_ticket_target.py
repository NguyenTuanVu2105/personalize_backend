from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from support.models import SupportTicket


class SupportTicketTarget(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True, unique=True)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="targets")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'support_ticket_target'
