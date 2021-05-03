from django.db import models
from django.db.models import QuerySet

from shop.constants import IGNORE_QUERY_ECOMMERCES, IGNORE_QUERY_STATUSES
from shop.constants.shop_status import ShopStatus


class BaseShopManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('ecommerce', 'currency')


class ShopQueryset(QuerySet):
    def is_active(self):
        return self.filter(status=ShopStatus.ACTIVE)

    def ecommerce_exclude(self):
        return self.exclude(ecommerce__name__in=IGNORE_QUERY_ECOMMERCES)

    def status_exclude(self):
        return self.exclude(status__in=IGNORE_QUERY_STATUSES)

ShopManager = BaseShopManager.from_queryset(ShopQueryset)
