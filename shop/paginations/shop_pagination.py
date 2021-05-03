from collections import OrderedDict

from rest_framework.response import Response

from HUB.paginations import EnhancedPageNumberPagination
from shop.constants.shop_status import SHOP_STATUS_CHOICES
from shop.models import Ecommerce
from shop.serializers import BriefEcommerceSerializer
from system_metadata.models import CurrencyExchangeRate
from system_metadata.serializers import BriefCurrencyExchangeRateSerializer


class ShopPagination(EnhancedPageNumberPagination):
    ECOMMERCE_ALLOWED_FILTER_FIELDS = ('owner', 'is_active')
    SHOP_CURRENCY_ALLOWED_FILTER_FIELDS = ('owner', 'is_active')

    def __init__(self):
        super().__init__()
        self.queryset = None
        self.options = None

    def paginate_queryset(self, queryset, request, view=None):
        self.options = self.get_options(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_options(self, queryset):
        ecommerce_options = self.get_ecommerce_options(queryset)
        currency_options = self.get_currency_options(queryset)
        options = OrderedDict([
            ("ecommerces", ecommerce_options),
            ("currencies", currency_options),
            ('status', SHOP_STATUS_CHOICES)
        ])
        return options

    def get_ecommerce_options(self, queryset):
        new_queryset = self._get_new_pure_queryset(queryset, self.ECOMMERCE_ALLOWED_FILTER_FIELDS)
        ecommerces = Ecommerce.objects.filter(id__in=new_queryset.values('ecommerce_id').distinct().order_by())
        return BriefEcommerceSerializer(ecommerces, many=True).data

    def get_currency_options(self, queryset):
        new_queryset = self._get_new_pure_queryset(queryset, self.SHOP_CURRENCY_ALLOWED_FILTER_FIELDS)
        shops = CurrencyExchangeRate.objects.filter(
            currency__in=new_queryset.values('currency__currency').distinct().order_by())
        return BriefCurrencyExchangeRateSerializer(shops, many=True).data

    def get_paginated_response(self, data):
        response_data_dict = super().get_paginated_response(data).data
        response_data_dict["options"] = self.options
        return Response(response_data_dict)
