from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from notification.models import MailHistory
from user.serializers.user import BriefUserSerializer


class MailHistorySerializer(ModelSerializer):
    type = CharField(source="verbose_type")
    status = CharField(source="verbose_status")
    owner = BriefUserSerializer()

    class Meta:
        model = MailHistory
        fields = ["id", "email", "type", "create_time", "send_time", "status", "owner"]
