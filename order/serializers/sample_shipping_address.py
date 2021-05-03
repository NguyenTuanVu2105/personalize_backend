from rest_framework.serializers import ModelSerializer

from order.models.sample_shipping_address import SampleShippingAddress


class SampleShippingAddressSerializer(ModelSerializer):
    class Meta:
        model = SampleShippingAddress
        fields = '__all__'
