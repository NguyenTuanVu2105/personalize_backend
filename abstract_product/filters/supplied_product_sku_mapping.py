from django_filters import FilterSet, CharFilter

from abstract_product.models.ffm_product_infos import FFMProductInfo


class SuppliedProductSkuMappingFilter(FilterSet):
    ph_product_sku = CharFilter(field_name='ph_product_sku', lookup_expr='istartswith')
    supplier_product_sku = CharFilter(field_name='supplier_product_sku', lookup_expr='istartswith')

    class Meta:
        model = FFMProductInfo
        fields = ('supplier_product_sku', 'ph_product_sku', 'supplier')
