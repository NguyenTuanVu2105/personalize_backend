from rest_framework.serializers import ModelSerializer, CharField

from notification.models import Message


class MessageSerializer(ModelSerializer):
    status = CharField(source="verbose_status")
    type = CharField(source="verbose_type")

    class Meta:
        model = Message
        fields = ["id", "title", "content", "create_time", "read_time", "status", "type"]
