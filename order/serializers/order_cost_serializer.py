from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from helper.choice_helpers import find_verbose_type_from_choices
from order.constants.fulfill_statuses import ORDER_FULFILL_STATUS_CHOICES, OrderPackFulfillStatus, ORDER_PACK_STATUS_VERBOSE_DICT
from order.models import OrderItem


class SampleOrderPack:
    def __init__(self, shipping_cost=0, production_cost=0, total_cost=0, fulfill_status=OrderPackFulfillStatus.PENDING):
        self.items = []
        self.shipping_cost = shipping_cost
        self.production_cost = production_cost
        self.total_cost = total_cost
        self.fulfill_status = fulfill_status

    def verbose_fulfill_status(self):
        return ORDER_PACK_STATUS_VERBOSE_DICT.get(self.fulfill_status)


class SampleOrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("quantity", "production_cost", "user_variant")


class SampleOrderPackSerializer(serializers.Serializer):
    shipping_cost = serializers.DecimalField(decimal_places=2, max_digits=11)
    production_cost = serializers.DecimalField(decimal_places=2, max_digits=11)
    total_cost = serializers.DecimalField(decimal_places=2, max_digits=11)
    fulfill_status = serializers.CharField(source="verbose_fulfill_status")
    items = SampleOrderItemSerializer(many=True)

    def create(self, validated_data):
        return SampleOrderPack(**validated_data)

    def update(self, instance, validated_data):
        instance.shipping_cost = validated_data.get('shipping_cost', instance.shipping_cost)
        instance.production_cost = validated_data.get('production_cost', instance.production_cost)
        instance.total_cost = validated_data.get('total_cost', instance.total_cost)
        fulfill_status = validated_data('fulfill_status', instance.fulfill_status)
        instance.fulfill_status = find_verbose_type_from_choices(ORDER_FULFILL_STATUS_CHOICES, fulfill_status)
        return instance
