from rest_framework.fields import FloatField
from rest_framework.serializers import ModelSerializer, CharField

from order.models import CancelShippingRequest, Order
from order.serializers.customer_info import CustomerInfoSerializer
from user.serializers.user import BriefUserSerializer


class BriefOrderSerializer(ModelSerializer):
    customer_info = CustomerInfoSerializer(many=False)

    class Meta:
        model = Order
        fields = (
            "id", "order_id", "order_number", "customer_info", "is_item_editable", "is_shipping_address_editable",
            "is_shipping_rate_editable", "is_cancellable", "tags", "note", "financial_status", "fulfill_status", "create_time",
            "update_time")


class CancelShippingRequestSerializer(ModelSerializer):
    order = BriefOrderSerializer()
    admin = BriefUserSerializer()
    user = BriefUserSerializer()
    status = CharField(source="verbose_status")
    total_shipping_cost = FloatField(source="get_total_shipping_cost")

    class Meta:
        model = CancelShippingRequest
        fields = (
            "id", "note", "order", "admin_note", "total_shipping_cost", "status", "approve_time", "create_time", "update_time", "admin",
            "user")
