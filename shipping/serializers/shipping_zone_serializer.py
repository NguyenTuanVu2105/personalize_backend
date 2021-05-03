from rest_framework import serializers

from shipping.models import ShippingZone


class BriefShippingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingZone
        fields = ('id', 'name', 'description')



