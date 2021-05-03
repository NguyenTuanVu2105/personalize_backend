from rest_framework import serializers

from ..models import UserAbstractVariantDefaultPrice


class UserAbstractVariantDefaultPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAbstractVariantDefaultPrice
        fields = "__all__"
