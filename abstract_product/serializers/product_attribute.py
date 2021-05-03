from rest_framework import serializers

from .product_attribute_value import ProductAttributeValueSerializer
from ..models import ProductAttribute


class ProductAttributeSerializer(serializers.ModelSerializer):
    child_attributes_value_set = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = ('id', 'product', 'name', 'type', 'child_attributes_value_set')
