from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from admin_tools.models.system_settings import SystemSetting


class SystemSettingSerializer(ModelSerializer):
    id = CharField(source="type")
    type = CharField(source="verbose_type")

    class Meta:
        model = SystemSetting
        fields = '__all__'
