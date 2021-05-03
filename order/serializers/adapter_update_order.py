from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from order.models.shipping_address import OrderShippingAddress
from order.serializers import GenericRelationOrderSerializer


class AdapterUpdateOrderShippingAddressSerializer(ModelSerializer):
    class Meta:
        model = OrderShippingAddress
        fields = ["first_name", "last_name", "phone", "address1", "address2", "city",
                  "province", "country", "country_code", "company", "zip"]


class AdapterUpdateOrderSerializer(GenericRelationOrderSerializer):
    shipping_address = AdapterUpdateOrderShippingAddressSerializer()
    id = serializers.IntegerField(source="order_id")

    class Meta(GenericRelationOrderSerializer.Meta):
        fields = ("id", "shipping_address")