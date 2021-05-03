from rest_framework import serializers

from abstract_product.models import AbstractProduct, ProductAttribute, ProductAttributeValue, AbstractProductMeta
from abstract_product.serializers.brief_abstract_product_category import BriefAbstractProductCategorySerializer


class AbstractProductMetaSerializer(serializers.ModelSerializer):
    shipping_meta = serializers.JSONField()

    class Meta:
        model = AbstractProductMeta
        fields = ('base_cost', 'short_description', 'shipping_meta', 'pricing_meta', 'design_note')


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ('label', 'value', 'sort_index')


class ProductAttributeSerializer(serializers.ModelSerializer):
    child_attributes_value_set = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = ('name', 'child_attributes_value_set')


class BriefAbstractProductSerializer(serializers.ModelSerializer):
    child_attributes = ProductAttributeSerializer(many=True)
    meta = AbstractProductMetaSerializer(read_only=True)
    categories = BriefAbstractProductCategorySerializer(many=True)

    class Meta:
        model = AbstractProduct
        fields = ('id', 'title', 'sku', 'is_active', 'combine_fusion', 'preview_image_url', 'child_attributes', 'meta',
                  'update_time', 'create_time', 'categories')
