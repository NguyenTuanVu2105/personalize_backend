import logging
import traceback

import django_filters

from HUB.filters import BaseCreatedTimeFilter
from ..models import UserProduct

logger = logging.getLogger(__name__)


class M2MFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        qs = qs.filter(shop=value)
        return qs


class CreatedTimeUserProductFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = UserProduct


class UserProductFilter(CreatedTimeUserProductFilter):
    shop = M2MFilter(field_name='shop')
    product = django_filters.NumberFilter(field_name='product')
    # type = django_filters.Filter(field_name='abstract_product__type')
    type = django_filters.Filter(method="abstract_type_filter")

    @staticmethod
    def abstract_type_filter(qs, value, *args):
        if not args:
            return qs
        else:
            qs = qs.filter(abstract_product__type__in=args[0].split(','))
            return qs

    class Meta(CreatedTimeUserProductFilter.Meta):
        model = UserProduct
        fields = CreatedTimeUserProductFilter.Meta.fields + ('shop', 'product', 'status', 'type')


class AdminProductFilter(CreatedTimeUserProductFilter):
    product = django_filters.NumberFilter(field_name='product')
    abstract = django_filters.CharFilter(method="abstract_product_filter")
    id_q = django_filters.NumberFilter(field_name='id', lookup_expr='startswith')
    user_variant_sku = django_filters.CharFilter(method="user_variant_sku_filter")

    @staticmethod
    def user_variant_sku_filter(qs, value, *args):
        if not args:
            return qs
        else:
            qs = qs.filter(user_product_variant_set__sku__contains=args[0])
            return qs

    @staticmethod
    def abstract_product_filter(queryset, value, *args, **kwargs):
        try:
            if args:
                queryset = queryset.filter(abstract_product__sku=args[0])

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.info(str(e))
            return queryset.none()

        return queryset

    class Meta(CreatedTimeUserProductFilter.Meta):
        model = UserProduct
        fields = CreatedTimeUserProductFilter.Meta.fields + (
            'id_q', 'user', 'product', 'status', 'abstract', 'user_variant_sku')
