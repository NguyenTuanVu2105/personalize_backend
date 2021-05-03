from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from HUB.viewsets.base import GenericViewSet
from event.constants.event_template_status import EventTemplateStatus
from event.models import EventTemplate
from event.serializers import BriefEventTemplateSerializer


class EventTemplateViewSet(GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = EventTemplate.objects.all()
    serializer_class = BriefEventTemplateSerializer
    filterset_fields = ['status', ]

    def get_queryset(self):
        return self.queryset.order_by('status', 'create_time')

    @action(methods=['GET'], detail=False, url_path='active')
    def get_all_active_event(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(status=EventTemplateStatus.ACTIVE)
        serializer = self.get_serializer_class()
        return Response(serializer(queryset, many=True).data)
