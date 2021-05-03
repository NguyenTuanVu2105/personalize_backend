from rest_framework import serializers

from user_product.models import EcommerceUnsyncVariant
from user_product.serializers.user_product_detail import UserVariantEcommerceSerializer


class EcommerceUnsyncVariantSerializer(serializers.ModelSerializer):
    user_variant_mapping = UserVariantEcommerceSerializer()

    class Meta:
        model = EcommerceUnsyncVariant
        fields = ('id', 'variant_meta', 'sku', 'is_active', 'user_variant_mapping')