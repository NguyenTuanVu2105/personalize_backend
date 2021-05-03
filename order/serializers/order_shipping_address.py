from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from order.models.shipping_address import OrderShippingAddress
from shipping.models import ShippingState


class OrderShippingAddressSerializer(ModelSerializer):
    name = serializers.StringRelatedField(source="full_name")

    class Meta:
        model = OrderShippingAddress
        fields = ["first_name", "last_name", "name", "phone", "address1", "address2", "city",
                  "province", "country", "country_code", "company", "zip"]


class FulfillServiceShippingAddressSerializer(ModelSerializer):
    address = serializers.StringRelatedField(source="address1")
    postal_code = serializers.StringRelatedField(source="zip")
    # state = serializers.StringRelatedField(source="province")
    state = serializers.SerializerMethodField()

    def get_state(self, obj):
        if obj.country_code == 'US':
            state = ShippingState.objects.filter(name=obj.province).first()
            if state:
                return state.code
        return obj.province

    class Meta:
        model = OrderShippingAddress
        fields = ["full_name", "phone", "address", "city", "state",
                  "country", "country_code", "postal_code", "address2"]
