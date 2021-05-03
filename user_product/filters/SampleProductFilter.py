import django_filters

from HUB.filters import BaseCreatedTimeFilter
from ..models import SampleProduct


class M2MFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        qs = qs.filter(shop=value)
        return qs


class SampleProductFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = SampleProduct


class AdminSampleProductFilter(BaseCreatedTimeFilter):
    abstract_product = django_filters.CharFilter(field_name='original_product__abstract_product__id')
    owner = django_filters.CharFilter(field_name='original_product__user')

    class Meta(BaseCreatedTimeFilter.Meta):
        model = SampleProduct
        fields = ('status', 'original_product_id', 'abstract_product', 'owner')

