from rest_framework import serializers

from abstract_product.serializers import ProductVariantSerializer
from user_product.models import UserVariant
from user_product.serializers.user_product import BriefUserProductSerializer
from user_product.serializers.user_variant_side_mockup import UserVariantSideMockupSerializer


class UserVariantSerializer(serializers.ModelSerializer):
    abstract_variant = ProductVariantSerializer()
    mockup_per_side = UserVariantSideMockupSerializer(many=True)
    title = serializers.CharField(source="product_title")

    class Meta:
        model = UserVariant
        fields = ('id', "title", "sku", 'user_product_id', 'abstract_variant', 'mockup_per_side')


class UserVariantWithPreviewSerializer(serializers.ModelSerializer):
    abstract_variant = ProductVariantSerializer()
    mockup_per_side = UserVariantSideMockupSerializer(many=True)
    title = serializers.CharField(source="product_title")
    preview_image_url = serializers.CharField(source='user_product.preview_image_url')
    seller_id = serializers.CharField(source='user_product.user_id')

    class Meta:
        model = UserVariant
        fields = ('id', "title", "sku", 'user_product_id', 'seller_id', 'type', 'abstract_variant', 'mockup_per_side',
                  'preview_image_url')


class UserVariantTYCardSerializer(serializers.ModelSerializer):
    user_product = BriefUserProductSerializer()

    class Meta:
        model = UserVariant
        fields = ('id', 'user_product')
