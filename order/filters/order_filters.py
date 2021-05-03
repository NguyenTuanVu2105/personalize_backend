import django_filters
from HUB.filters import BaseCreatedTimeFilter
from order.models import Order


class CreatedTimeOrderFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = Order


class MultiShopFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        shops = value.split(',')
        return qs.filter(shop_id__in=shops)


class OrderFilter(CreatedTimeOrderFilter):
    shop_id = MultiShopFilter()

    class Meta(CreatedTimeOrderFilter.Meta):
        model = Order
        fields = CreatedTimeOrderFilter.Meta.fields + ('fulfill_status', 'financial_status', 'shop_id')
