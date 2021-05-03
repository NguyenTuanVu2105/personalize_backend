from rest_framework import serializers

from shipping.models import ShippingCountry
from shipping.serializers import BriefShippingStateSerializer, BriefShippingZoneSerializer


class BriefShippingCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCountry
        fields = ('id', 'code', 'name')


class ShippingCountrySerializer(serializers.ModelSerializer):
    states = BriefShippingStateSerializer(many=True)
    zone = BriefShippingZoneSerializer()
    class Meta:
        model = ShippingCountry
        fields = ('id', 'code', 'name', 'states', 'zone')
