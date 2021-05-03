from HUB.filters import BaseCreatedTimeFilter
from billing.models import Invoice


class InvoiceFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = Invoice
        fields = BaseCreatedTimeFilter.Meta.fields + ('status',)
