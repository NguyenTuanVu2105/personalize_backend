from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from support.models import SupportTicket


class SupportTicketConversation(RandomIDModel):
    conversation_id = models.BigIntegerField(db_index=True, unique=True)
    meta = JSONField()
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="conversations")
    create_time = models.DateTimeField(db_index=True)
    update_time = models.DateTimeField(auto_now=True)
    customer_send = models.BooleanField(default=False)

    class Meta:
        db_table = 'support_ticket_conversation'
        ordering = ["create_time"]
