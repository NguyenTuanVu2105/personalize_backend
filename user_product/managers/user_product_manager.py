from django.db import models
from django.db.models import QuerySet

from abstract_product.constants import AbstractType
from user_product.constants import IGNORE_QUERY_STATUSES, UserProductStatus


class BaseUserProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user')


class UserProductQueryset(QuerySet):
    def is_active(self):
        return self.filter(status=UserProductStatus.ACTIVE)

    def status_exclude(self):
        return self.exclude(status__in=IGNORE_QUERY_STATUSES)

    def product_only(self):
        return self.filter(abstract_product__type__in=[AbstractType.AOP_PRODUCT, AbstractType.FLAT_PRODUCT])


UserProductManager = BaseUserProductManager.from_queryset(UserProductQueryset)
