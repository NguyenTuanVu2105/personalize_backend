import logging

from rest_framework import serializers

from abstract_product.serializers.abstract_product_mockup_infos import AbstractProductMockupInfoSerializer
from abstract_product.serializers.abstract_product_side import AbstractProductSideSerializer
from .abstract_product_meta import AbstractProductMetaSerializer
from .abstract_product_variant import BriefProductVariantSerializer
from .product_attribute import ProductAttributeSerializer
from ..models import AbstractProduct

logger = logging.getLogger(__name__)


class ProductSerializer(serializers.ModelSerializer):
    abstract_product_variants = BriefProductVariantSerializer(many=True)
    child_attributes = ProductAttributeSerializer(many=True)
    meta = AbstractProductMetaSerializer(read_only=True)
    mockup_infos = AbstractProductMockupInfoSerializer(many=True)
    sides = AbstractProductSideSerializer(many=True)

    class Meta:
        model = AbstractProduct
        fields = (
            'id', 'title', 'type', 'sku', 'preview_image_url', 'is_active', 'meta', 'child_attributes', 'sides',
            'mockup_infos',
            'abstract_product_variants')


class ProductBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractProduct
        fields = ('id', 'title', 'sku', 'is_active', 'type', 'preview_image_url')
