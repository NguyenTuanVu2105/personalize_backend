import django_filters

from HUB.filters import BaseCreatedTimeFilter
from order.models.order_invallid import OrderInvalid
from shop.models import Shop


class ShopFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        shop = Shop.objects.filter(url=value).first()
        qs = qs.filter(shop=shop)
        return qs


class OrderInvalidFilter(BaseCreatedTimeFilter):
    shop_url = ShopFilter(field_name='shop')

    class Meta(BaseCreatedTimeFilter.Meta):
        model = OrderInvalid
        fields = BaseCreatedTimeFilter.Meta.fields + ("shop_url", )
