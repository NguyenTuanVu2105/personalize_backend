from rest_framework import mixins

from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from service_communication.constants.request_type import REQUEST_TYPES_LIST
from service_communication.models import ServiceCommunicationLog
from service_communication.serializers.request_log_serializers import BriefRequestLogSerializer


class RequestLogViewSet(SearchableListModelMixin,
                        mixins.RetrieveModelMixin,
                        AdminGenericViewSet):
    queryset = ServiceCommunicationLog.objects.all()
    serializer_class = BriefRequestLogSerializer
    filterset_fields = ('type', 'status_code', 'object_id', 'webhook_job')

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_webhook_job_view', ]))
    def list(self, request, *args, **kwargs):
        self.serializer_class = BriefRequestLogSerializer
        response = super().list(request, *args, **kwargs)
        response_data = response.data
        response_data["request_types"] = REQUEST_TYPES_LIST
        return response
