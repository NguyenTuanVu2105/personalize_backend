from django_filters import Filter

from HUB.filters import BaseCreatedTimeFilter
from support.models import SupportTicket


class MultiStatusFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        result = SupportTicket.objects.none()
        for v in values:
            tmp_queryset = qs.filter(status=v)
            result = result | tmp_queryset

        return result


class CreatedTimeTicketFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = SupportTicket


class TicketFilter(CreatedTimeTicketFilter):
    status = MultiStatusFilter()

    class Meta:
        model = SupportTicket
        fields = ['status', 'read']
