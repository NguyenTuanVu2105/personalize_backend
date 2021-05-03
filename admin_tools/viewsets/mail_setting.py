from rest_framework.mixins import ListModelMixin, UpdateModelMixin

from HUB.viewsets.base import AdminGenericViewSet
from admin_tools.models import MailSetting
from admin_tools.serializers.mail_settings import MailSettingSerializer


class MailSettingViewSet(ListModelMixin, UpdateModelMixin, AdminGenericViewSet):
    queryset = MailSetting.objects.all()
    serializer_class = MailSettingSerializer