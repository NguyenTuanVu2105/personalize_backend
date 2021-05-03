from HUB.filters import BaseCreatedTimeFilter
from django_filters import CharFilter

from notification.models import MailHistory


class MailHistoryFilter(BaseCreatedTimeFilter):
    email = CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = MailHistory
        fields = BaseCreatedTimeFilter.Meta.fields + ('type', 'email',)
