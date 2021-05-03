from django.contrib.postgres.aggregates import ArrayAgg

from HUB import logger
from shop.filters import ShopFilter
from shop.models import Shop, ShopTag
import django_filters

from user.filters import UserFieldFilter


class CheckLocationFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        qs = qs.filter(location_change__type=value, location_change__is_resolve=False)
        return qs


# def filter_check_location(queryset, type):
#     return queryset.filter(location_change__type=type)

class ShopOwnerFilter(ShopFilter):
    owner = UserFieldFilter(field_name='owner', lookup_expr='icontains')
    tags = django_filters.CharFilter(method='filter_tags')
    check_location_type = CheckLocationFilter()

    @staticmethod
    def filter_tags(queryset, value, *args, **kwargs):
        try:
            if args:
                temp = ShopTag.objects.values('shop').annotate(tags=ArrayAgg('tag')).order_by()
                shop_id = [item['shop'] for item in temp if
                           all([tag_value in item['tags'] for tag_value in args[0].split(',')])]
                queryset = queryset.filter(id__in=shop_id)
        except Exception as e:
            logger.info(str(e))
            return queryset.none()
        return queryset

    class Meta:
        model = Shop
        fields = ShopFilter.Meta.fields + ('owner', 'check_location_type', 'status')
