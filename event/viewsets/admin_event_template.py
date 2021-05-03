from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from event.constants.event_template_status import EventTemplateStatus
from event.models import EventTemplate
from event.serializers import EventTemplateSerializer


class AdminEventTemplateViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                                UpdateModelMixin, AdminGenericViewSet):
    queryset = EventTemplate.objects.all()
    serializer_class = EventTemplateSerializer
    filterset_fields = ['status', ]

    @action(methods=['GET'], detail=False, url_path='all')
    def get_all(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        queryset = self.filter_queryset(queryset=self.queryset)
        return Response(serializer(queryset, many=True).data)

    def bulk_change_status(self, ids, new_status):
        response_data = []
        for event_id in ids:
            event = EventTemplate.objects.get(pk=event_id)
            event.status = new_status
            event.save()
            response_data.append({
                "event": event.id,
                "name": event.name,
                "success": True
            })
        return Response({"results": response_data})

    @action(methods=["PUT", "PATCH"], detail=False, url_path="bulk-activate")
    def bulk_activate(self, request, *args, **kwargs):
        request_data = request.data
        event_ids = request_data['ids']
        return self.bulk_change_status(event_ids, EventTemplateStatus.ACTIVE)

    @action(methods=["PUT", "PATCH"], detail=False, url_path="bulk-deactivate")
    def bulk_deactivate(self, request, *args, **kwargs):
        request_data = request.data
        event_ids = request_data['ids']
        return self.bulk_change_status(event_ids, EventTemplateStatus.INACTIVE)
