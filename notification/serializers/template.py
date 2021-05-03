from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from admin_tools.serializers.custom_mail_seder import CustomMailSenderSerializer
from admin_tools.serializers.mail_settings import MailSettingSerializer
from notification.models import Template


class TemplateSerializer(ModelSerializer):
    type = CharField(source="verbose_type")
    id = CharField(source="type")

    class Meta:
        model = Template
        fields = ["id", "type", "message_title", "message_content", "mail_title", "mail_content", "send_email", "send_message", "parameter_list", "is_send_custom_mail", "mail_sender"]
        read_only_fields = ["id", "type"]
        extra_kwargs = {
            'id': {'read_only': True},
            'type': {'read_only': True}
        }
