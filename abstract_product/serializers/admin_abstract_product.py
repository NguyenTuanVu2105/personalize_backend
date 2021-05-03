import logging

from rest_framework import serializers

from abstract_product.models import ProductAttributeValue, AbstractProductVariant, AbstractProductSide, \
    AbstractProductMockupInfo, ProductAttribute, AbstractProductMeta
from abstract_product.serializers.brief_abstract_product_category import BriefAbstractProductCategorySerializer
from ..models import AbstractProduct

logger = logging.getLogger(__name__)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ('id', 'label', 'value', 'attribute', 'sort_index', 'is_active')


class ProductAttributeSerializer(serializers.ModelSerializer):
    child_attributes_value_set = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = ('id', 'product', 'name', 'type', 'child_attributes_value_set')


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes_value = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = AbstractProductVariant
        fields = ('id', 'product', 'sku', 'description', 'attributes_value', 'mockup_info')


class AbstractProductSideSerializer(serializers.ModelSerializer):
    constraints = serializers.JSONField()

    class Meta:
        model = AbstractProductSide
        fields = ('id', 'type', 'constraints', 'fusion_size', 'enable_background_color')


class AbstractProductMockupInfoSerializer(serializers.ModelSerializer):
    preview = serializers.JSONField()

    class Meta:
        model = AbstractProductMockupInfo
        fields = ('id', 'name', 'preview', 'meta', 'preview_meta')


class AbstractProductMetaSerializer(serializers.ModelSerializer):
    pricing_meta = serializers.JSONField()

    class Meta:
        model = AbstractProductMeta
        fields = (
            'id', 'base_cost', 'description', 'pricing_meta', 'abstract_product', 'short_description', 'shipping_meta',
            'design_note', 'fusion_meta')


class AdminAbstractProductSerializer(serializers.ModelSerializer):
    abstract_product_variants = ProductVariantSerializer(many=True)
    child_attributes = ProductAttributeSerializer(many=True)
    meta = AbstractProductMetaSerializer(read_only=True)
    mockup_infos = AbstractProductMockupInfoSerializer(many=True)
    sides = AbstractProductSideSerializer(many=True)
    categories = BriefAbstractProductCategorySerializer(many=True)

    class Meta:
        model = AbstractProduct
        fields = ('id', 'title', 'preview_image_url', 'is_active', 'type', 'meta', 'categories', 'abstract_product_variants',
                  'child_attributes', 'sides', 'mockup_infos', 'update_time', 'is_catalog_visible',
                  'active_mockup_version')


class AdminAbstractProductSimpleSerializer(serializers.ModelSerializer):
    sides = AbstractProductSideSerializer(many=True)

    class Meta:
        model = AbstractProduct
        fields = ('id', 'title', 'preview_image_url', 'is_active', 'sides', 'type')


class AdminAbstractProductPreviewAndTemplateSerializer(serializers.ModelSerializer):
    template_meta = serializers.JSONField(source="meta.template_meta")
    mockup_infos = AbstractProductMockupInfoSerializer(many=True)

    class Meta:
        model = AbstractProduct
        fields = ('id', 'title', 'preview_image_url', 'template_meta', 'mockup_infos')


class AdminAbstractProductSortingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractProduct
        fields = ('id', 'title', 'preview_image_url', 'sort_index')
