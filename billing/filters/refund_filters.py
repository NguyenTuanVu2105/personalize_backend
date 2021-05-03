import django_filters

from HUB.filters import BaseCreatedTimeFilter
from billing.models import Refund


class RefundFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = Refund
        fields = BaseCreatedTimeFilter.Meta.fields + ('refund_type', 'status')



