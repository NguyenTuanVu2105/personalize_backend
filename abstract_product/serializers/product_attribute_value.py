from rest_framework import serializers

from abstract_product.models import ProductAttribute
from ..models import ProductAttributeValue


class BriefProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('id', 'name')


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ('id', 'label', 'value', 'attribute', 'sort_index')


class AttributeValueWithAttributeAndLabelSerializer(serializers.ModelSerializer):
    attribute = BriefProductAttributeSerializer()

    class Meta:
        model = ProductAttributeValue
        fields = ('id', 'label', 'attribute')


class FulfillProductAttributeValueSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='attribute')
    key = serializers.StringRelatedField(source='attribute.name')
    attribute_id = serializers.StringRelatedField(source='attribute.id')

    class Meta:
        model = ProductAttributeValue
        fields = ('name', 'key', 'value', 'attribute_id')


class AdminProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ('id', 'label', 'is_active', 'value', 'attribute', 'sort_index')
        read_only_fields = ['id', 'sort_index', 'attribute']
