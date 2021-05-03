from rest_framework import serializers

from ..models import AbstractProductVariantAttribute


class AbstractProductVariantAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractProductVariantAttribute
        fields = ('id', 'variant', 'attribute_value')
