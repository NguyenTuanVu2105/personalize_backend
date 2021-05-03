from collections import OrderedDict

from rest_framework.response import Response

from HUB.paginations import EnhancedPageNumberPagination
from shop.models import Shop
from shop.serializers.shop import BriefShopSerializer


class OrderPagination(EnhancedPageNumberPagination):
    SHOP_ALLOWED_FILTER_FIELDS = ('owner', 'is_active')

    def __init__(self):
        super().__init__()
        self.queryset = None
        self.options = None

    def paginate_queryset(self, queryset, request, view=None):
        self.options = self.get_options(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_options(self, queryset):
        shop_options = self.get_shop_options(queryset)
        options = OrderedDict([
            ("shops", shop_options)
        ])
        return options

    def get_shop_options(self, queryset):
        new_queryset = self._get_new_pure_queryset(queryset, self.SHOP_ALLOWED_FILTER_FIELDS)
        shops = Shop.objects.filter(id__in=new_queryset.values('shop_id').distinct().order_by())
        return BriefShopSerializer(shops, many=True).data

    def get_paginated_response(self, data):
        response_data_dict = super().get_paginated_response(data).data
        response_data_dict["options"] = self.options
        return Response(response_data_dict)
