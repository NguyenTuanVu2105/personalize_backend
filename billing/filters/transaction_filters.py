import django_filters

from HUB.filters import BaseCreatedTimeFilter
from billing.models import Transaction, Invoice, Refund


class TransactionFilter(BaseCreatedTimeFilter):
    order_id = django_filters.CharFilter(method='filter_order_id')

    @staticmethod
    def filter_order_id(queryset, value, *args, **kwargs):
        if not args:
            return queryset
        else:
            order_id = int(args[0])
            invoices = Invoice.objects.filter(packs__order_pack__order_id=order_id)
            refunds = Refund.objects.filter(object_id=order_id)
            ids = list(invoices.values_list('id', flat=True).distinct().order_by())
            ids += refunds.values_list('id', flat=True).distinct().order_by()
            return queryset.filter(object_id__in=ids)

    class Meta(BaseCreatedTimeFilter.Meta):
        model = Transaction
        fields = BaseCreatedTimeFilter.Meta.fields + ('type', 'status')


class CreatedTimeTransactionFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = Transaction
