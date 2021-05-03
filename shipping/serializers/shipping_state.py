from rest_framework import serializers

from shipping.models import ShippingState


class BriefShippingStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingState
        fields = ('id', 'code', 'name')
