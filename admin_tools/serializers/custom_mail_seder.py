from rest_framework.serializers import ModelSerializer

from admin_tools.models.custom_mail_sender import CustomMailSender


class CustomMailSenderSerializer(ModelSerializer):
    class Meta:
        model = CustomMailSender
        fields = '__all__'
