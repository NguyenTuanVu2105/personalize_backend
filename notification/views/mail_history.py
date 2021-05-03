from rest_framework import mixins
from rest_framework.response import Response

from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from notification.enums.message_types import MESSAGE_TYPES
from notification.filter.mail_history_filter import MailHistoryFilter
from notification.models import MailHistory
from notification.serializers.mail_history import MailHistorySerializer


class MailHistoryViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         AdminGenericViewSet):
    queryset = MailHistory.objects.select_related('owner').all()
    filterset_class = MailHistoryFilter
    serializer_class = MailHistorySerializer

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_mail_history_view', ]))
    def list(self, request, *args, **kwargs):
        data = super().list(self, request, *args, **kwargs).data
        data['option'] = {'types': MESSAGE_TYPES}
        return Response(data)

    @method_permission_required(get_permissions(['admin_mail_history_view', ]))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)
