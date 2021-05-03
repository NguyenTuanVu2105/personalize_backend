from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from billing.models import Transaction, Invoice, Refund
from order.models import Order
from user.serializers.user import BriefUserSerializer


class TransactionSerializer(ModelSerializer):
    object = serializers.JSONField(source='get_content_object_info')
    payment_method = serializers.JSONField(source='get_payment_method')

    class Meta:
        model = Transaction
        fields = (
            "id", "object", "payment_method", "type", "amount", "status", "create_time")


class SimpleTransactionSerializer(ModelSerializer):
    object = serializers.JSONField(source='get_content_object_info')
    payment_method = serializers.JSONField(source='get_payment_method')

    class Meta:
        model = Transaction
        fields = (
            "id", "object", "payment_method", "type", "amount", "status", "create_time")


class AdminTransactionSerializer(ModelSerializer):
    object = serializers.JSONField(source='get_content_object_info')
    payment_method = serializers.JSONField(source='get_payment_method')
    owner = BriefUserSerializer(source='get_owner')

    order_ids = serializers.ListField()

    class Meta:
        model = Transaction
        fields = (
            "id", 'order_ids', "object", "owner", "payment_method", "type", "amount", "status", "create_time", "detail")
