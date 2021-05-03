from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from user.models import UserSettings
from user.serializers import UserSettingsSerializer


class AdminUserSettingsViewSet(AdminGenericViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer

    @action(methods=['get'], detail=False, url_path='get-by-user')
    def get_by_user(self, request):
        user_id = request.GET.get('user_id')
        return Response(self.get_serializer(self.queryset.filter(user_id=user_id).first()).data)
