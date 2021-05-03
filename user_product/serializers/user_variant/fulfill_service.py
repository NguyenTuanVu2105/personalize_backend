from rest_framework import serializers

from abstract_product.serializers import FulfillServiceProductVariantSerializer
from user_product.models import UserVariant, UserProduct
from user_product.serializers.user_variant_side_mockup import FulfillUserVariantSideMockupSerializer


class FulfillServiceUserProductSerializer(serializers.ModelSerializer):
    preview = serializers.StringRelatedField(source='preview_image_url')

    class Meta:
        model = UserProduct
        fields = ('id', 'title', 'description', 'preview')


class FulfillServiceUserVariantSerializer(serializers.ModelSerializer):
    product = FulfillServiceUserProductSerializer(source="user_product")
    previews = FulfillUserVariantSideMockupSerializer(many=True, source="mockup_per_side")
    variant = FulfillServiceProductVariantSerializer(source="abstract_variant")

    class Meta:
        model = UserVariant
        fields = ("sku", 'product', 'variant', 'previews')

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['variant']['id'] = obj.id
        if obj.user_product and obj.user_product.abstract_product and obj.user_product.abstract_product.title:
            representation['variant'][
                'sku'] = f"{representation['variant']['sku']} ({obj.user_product.abstract_product.title})"
        return representation
