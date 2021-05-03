from rest_framework import serializers

from shipping.models import ShippingRate


class BriefShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = ('id', 'name', 'slug', 'description', 'is_default')
