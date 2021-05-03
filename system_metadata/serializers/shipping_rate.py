from rest_framework.serializers import ModelSerializer

from shipping.models.shipping_rate import ShippingRate


class ShippingRateSerializer(ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = ['id', 'name', 'slug', 'description']
