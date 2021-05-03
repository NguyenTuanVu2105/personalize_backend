from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField

from order.models import OrderItem
from user_product.serializers import FulfillServiceUserVariantSerializer
from user_product.serializers.user_variant.base import UserVariantWithPreviewSerializer


class OrderItemSerializer(ModelSerializer):
    variant = UserVariantWithPreviewSerializer(source="user_variant")
    fulfill_status = CharField(source="verbose_fulfill_status")

    class Meta:
        model = OrderItem
        fields = ("id", "quantity", "price", "discount", "currency", "production_cost", "variant", "fulfill_status", "base_cost", "extra_cost")


class FulfillServiceOrderItemSerializer(ModelSerializer):
    user_variant = FulfillServiceUserVariantSerializer()
    price = serializers.DecimalField(source='production_cost', decimal_places=2, max_digits=11)

    class Meta:
        model = OrderItem
        fields = ("id", "quantity", "price", "discount", "currency", "user_variant")

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        variant_representation = representation.pop('user_variant')
        for key in variant_representation:
            representation[key] = variant_representation[key]
        return representation


class MerchantServiceOrderItemSerializer(ModelSerializer):
    id = CharField(source="item_id")

    class Meta:
        model = OrderItem
        fields = ("id",)
