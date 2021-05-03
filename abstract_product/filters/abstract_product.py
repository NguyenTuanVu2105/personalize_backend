import logging
import traceback

import django_filters
from django_filters import FilterSet

from ..models import AbstractProduct

logger = logging.getLogger(__name__)


class AdminAbstractProductFilter(FilterSet):
    abstract = django_filters.CharFilter(method="abstract_product_filter")

    @staticmethod
    def abstract_product_filter(queryset, value, *args, **kwargs):
        try:
            if args:
                queryset = queryset.filter(sku=args[0])

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.info(str(e))
            return queryset.none()

        return queryset

    class Meta:
        model = AbstractProduct
        fields = ('title', 'categories', 'is_active', 'abstract')
