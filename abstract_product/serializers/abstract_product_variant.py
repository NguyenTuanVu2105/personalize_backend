from rest_framework import serializers

from shipping.models import ShippingCostAbstractVariant
from .product_attribute_value import ProductAttributeValueSerializer, FulfillProductAttributeValueSerializer, \
    AttributeValueWithAttributeAndLabelSerializer
from ..models import AbstractProductVariant


class BriefProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractProductVariant
        fields = ('id', 'product', 'sku', 'description', 'attributes_value', 'mockup_info')


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes_value = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = AbstractProductVariant
        fields = ('id', 'product', 'sku', 'description', 'attributes_value', 'mockup_info')


class ShippingCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCostAbstractVariant
        fields = (
            'shipping_zone', 'shipping_rate', 'shipping_cost_base', 'shipping_cost_additional', 'production_cost_base',
            'production_cost_additional', 'id')


class ProductVariantPriceSerializer(serializers.ModelSerializer):
    shipping_costs = ShippingCostSerializer(many=True)

    class Meta:
        model = AbstractProductVariant
        fields = ('id', 'sku', 'shipping_costs')


class ProductVariantPriceAttributeSerializer(serializers.ModelSerializer):
    shipping_costs = ShippingCostSerializer(many=True)
    attributes_value = AttributeValueWithAttributeAndLabelSerializer(many=True)

    class Meta:
        model = AbstractProductVariant
        fields = ('id', 'sku', 'shipping_costs', 'attributes_value')


class FulfillServiceProductVariantSerializer(serializers.ModelSerializer):
    options = FulfillProductAttributeValueSerializer(many=True, source="attributes_value")
    title = serializers.SerializerMethodField()

    class Meta:
        model = AbstractProductVariant
        fields = ('id', 'sku', 'title', 'options')

    def get_title(self, obj):
        return obj.description
