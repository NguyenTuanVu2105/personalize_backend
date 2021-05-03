from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from admin_tools.models.mail_settings import MailSetting


class MailSettingSerializer(ModelSerializer):
    class Meta:
        model = MailSetting
        fields = '__all__'
