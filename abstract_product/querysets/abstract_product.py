from django.db.models import Prefetch

from ..models import AbstractProductVariant, ProductAttribute, ProductAttributeValue


def abstract_product_queryset(base_queryset):
    queryset = base_queryset \
        .select_related("meta") \
        .prefetch_related(
        Prefetch(
            "abstract_product_variants",
            queryset=AbstractProductVariant.objects
                .filter(is_active=True)
                .prefetch_related("attributes_value"),
        ),
        Prefetch(
            "child_attributes",
            queryset=ProductAttribute.objects.order_by('sort_index')
                .prefetch_related(
                Prefetch(
                    "child_attributes_value_set",
                    queryset=ProductAttributeValue.objects.filter(is_active=True).order_by('sort_index'),
                )),
        ),
        'mockup_infos',
        'sides'
    )
    return queryset
