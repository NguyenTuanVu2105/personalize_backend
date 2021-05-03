from rest_framework import serializers

from shop.serializers import ShopSerializer
from user_product.models import EcommerceUnsyncedProduct
from user_product.serializers.shop_ecommerce_unsync_variant import EcommerceUnsyncVariantSerializer


class EcommerceUnsyncProductSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()

    class Meta:
        model = EcommerceUnsyncedProduct
        fields = ('id', 'product_meta', 'title', 'description', 'shop', 'create_time', 'update_time', 'is_active')


class EcommerceUnsyncProductDetailSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    ecommerce_variant_set = EcommerceUnsyncVariantSerializer(many=True)

    class Meta:
        model = EcommerceUnsyncedProduct
        fields = ('id', 'product_meta', 'title', 'description', 'shop', 'create_time', 'update_time', 'is_active',
                  'ecommerce_variant_set')
