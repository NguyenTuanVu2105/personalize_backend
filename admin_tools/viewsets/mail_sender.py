from rest_framework.mixins import ListModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin

from HUB.viewsets.base import AdminGenericViewSet
from admin_tools.models.custom_mail_sender import CustomMailSender
from admin_tools.serializers.custom_mail_seder import CustomMailSenderSerializer
from notification.models import Template

class CustomMailSenderViewSet(ListModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin, AdminGenericViewSet):
    queryset = CustomMailSender.objects.all()
    serializer_class = CustomMailSenderSerializer

    def destroy(self, request, *args, **kwargs):
        mail = self.get_object()
        Template.objects.filter(mail_sender=mail).update(mail_sender=None)
        return super().destroy(request, *args, **kwargs)