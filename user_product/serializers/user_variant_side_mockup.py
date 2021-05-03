from rest_framework import serializers

from ..models import UserVariantSideMockup


class UserVariantSideMockupSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product_side.id')
    product_side = serializers.ReadOnlyField(source='product_side.type')

    class Meta:
        model = UserVariantSideMockup
        fields = ('id', 'product_side', 'mockup_url', "user_variant")


class FulfillUserVariantSideMockupSerializer(UserVariantSideMockupSerializer):
    class Meta(UserVariantSideMockupSerializer.Meta):
        fields = ('product_side', 'mockup_url')
