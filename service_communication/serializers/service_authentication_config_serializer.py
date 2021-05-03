from rest_framework.serializers import ModelSerializer

from service_communication.models import ServiceAuthenticationConfig


class ServiceAuthenticationConfigSerializer(ModelSerializer):
    class Meta:
        model = ServiceAuthenticationConfig
        fields = '__all__'
