from rest_framework import serializers
from rest_framework.fields import CharField

from support.models import SupportTicket, SupportTicketConversation


class BriefTicketSupportSerializer(serializers.ModelSerializer):
    status = CharField(source="verbose_status")

    class Meta:
        model = SupportTicket
        fields = (
            'id', 'ticket_id', 'status', 'subject', 'description', 'url', 'create_time',
            'update_time', 'attachments', 'read', 'customer_last_reply')


class TicketSupportConversationSerializer(serializers.ModelSerializer):
    meta = serializers.JSONField()

    class Meta:
        model = SupportTicketConversation
        fields = ('id', 'meta', 'create_time', 'customer_send')
