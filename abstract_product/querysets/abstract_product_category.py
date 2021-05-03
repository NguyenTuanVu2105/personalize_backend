from django.db.models import Prefetch

from ..models.abstract_product import AbstractProduct


def abstract_product_category_queryset(base_queryset):
    queryset = base_queryset.prefetch_related(
        Prefetch(
            "child_abstract_products",
            queryset=AbstractProduct.objects.product_only().active_visible_filter().order_by(
                'sort_index').select_related("meta").prefetch_related("categories", "child_attributes",
                                                                      "child_attributes__child_attributes_value_set")))
    return queryset
