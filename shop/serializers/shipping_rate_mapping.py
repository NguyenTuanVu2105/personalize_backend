from rest_framework.serializers import ModelSerializer

from shop.models import ShopShippingRateMapping


class ShopShippingRateMappingSerializer(ModelSerializer):
    class Meta:
        model = ShopShippingRateMapping
        fields = ['id', 'shop', 'e_commerce_shipping_rate_name', 'shipping_rate', 'countries', 'create_time', 'update_time']
