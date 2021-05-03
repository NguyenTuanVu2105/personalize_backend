from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from service_communication.constants.authenticated_service import AUTHENTICATION_SERVICE_TYPES
from service_communication.constants.authentication_type import AUTHENTICATION_TYPES
from service_communication.models import ServiceAuthenticationConfig
from service_communication.serializers import ServiceAuthenticationConfigSerializer


class ServiceAuthenticationConfigViewSet(AdminGenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = ServiceAuthenticationConfig.objects.all()
    serializer_class = ServiceAuthenticationConfigSerializer

    def list(self, request, *args, **kwargs):
        resp_dict = super(ServiceAuthenticationConfigViewSet, self).list(request, *args, **kwargs).data
        resp_dict['options'] = {
            'services': AUTHENTICATION_SERVICE_TYPES,
            'types': AUTHENTICATION_TYPES,
        }
        return Response(resp_dict)
