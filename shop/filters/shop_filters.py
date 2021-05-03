import logging
import traceback

import django_filters

from HUB.filters import BaseCreatedTimeFilter
from shop.models import Shop
from user_product.models import UserProduct

logger = logging.getLogger(__name__)


class CreatedTimeShopFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = Shop


class ShopFilter(CreatedTimeShopFilter):
    currency = django_filters.CharFilter(field_name="currency__currency")
    ecommerce = django_filters.CharFilter(field_name="ecommerce__name")
    product = django_filters.CharFilter(method="has_product")

    def has_product(self, queryset, value, *args, **kwargs):
        try:
            if args:
                user_product = UserProduct.objects.get(pk=args[0])
                queryset = queryset.exclude(id__in=user_product.shops.all())

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.info(str(e))
            return queryset.none()

        return queryset

    class Meta(CreatedTimeShopFilter.Meta):
        model = Shop
        fields = CreatedTimeShopFilter.Meta.fields + ('ecommerce', 'currency', 'status')
