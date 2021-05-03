from rest_framework import serializers

from abstract_product.models import AbstractProductCategory
from abstract_product.serializers.brief_abstract_product import BriefAbstractProductSerializer


class AbstractProductCategorySerializer(serializers.ModelSerializer):
    child_abstract_products = serializers.SerializerMethodField()

    @staticmethod
    def get_child_abstract_products(instance):
        abstract_products = instance.child_abstract_products.exclude(is_catalog_visible=False)
        return [BriefAbstractProductSerializer(abstract_product).data for abstract_product in abstract_products]

    class Meta:
        model = AbstractProductCategory
        fields = ('id', 'is_active', 'force_active', 'child_abstract_products', 'sort_index', 'title', 'preview_image_url')
