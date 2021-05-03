from django.db import models
from django.db.models import QuerySet, Q

from user_product.constants import SampleProductStatus


class BaseSampleProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('original_product')


class SampleProductQueryset(QuerySet):
    def is_active(self):
        return self.filter(status=SampleProductStatus.ACTIVE)

    def is_highlight(self):
        return self.is_active().filter(is_highlight=True)

    def is_not_highlight(self):
        return self.is_active().filter(is_highlight=False)

    def unused_filter(self, user):
        return self.exclude(Q(created_user_products__user_id=user) | Q(original_product__user_id=user)).distinct()


SampleProductManager = BaseSampleProductManager.from_queryset(SampleProductQueryset)
