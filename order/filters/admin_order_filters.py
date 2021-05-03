from django.contrib.postgres.aggregates import BoolAnd

from HUB.filters import BaseCreatedTimeFilter
from order.models import Order
from django_filters import BooleanFilter


class AdminOrderFilter(BaseCreatedTimeFilter):
    manually_update = BooleanFilter(method='check_manually')

    def check_manually(self, queryset, name, value):
        return queryset.annotate(manually=BoolAnd('packs__fulfillment_order_packs__manually_update')) \
            .filter(manually=value)

    class Meta(BaseCreatedTimeFilter.Meta):
        model = Order
        fields = BaseCreatedTimeFilter.Meta.fields + (
            'fulfill_status', 'financial_status', 'shop__owner', 'shop', 'manually_update', 'is_delivered_order')
