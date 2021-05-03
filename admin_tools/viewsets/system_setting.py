from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from admin_tools.models import SystemSetting
from admin_tools.serializers import SystemSettingSerializer


class SystemSettingViewSet(ListModelMixin, RetrieveModelMixin, AdminGenericViewSet):
    queryset = SystemSetting.objects.order_by('type')
    serializer_class = SystemSettingSerializer

    @action(methods=['GET', ], detail=False, url_path='all')
    def get_all(self, request):
        return Response(self.serializer_class(self.get_queryset(), many=True).data)

    @action(methods=['PATCH', ], detail=True, url_path='update-value')
    def update_value(self, request, *args, **kwargs):
        setting = self.get_object()
        setting.value = request.data.get('value') or setting.value
        setting.save()
        return Response(self.get_serializer(setting).data)
