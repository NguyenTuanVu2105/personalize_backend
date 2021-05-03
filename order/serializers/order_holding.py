from rest_framework.serializers import ModelSerializer

from order.models import OrderHolding


class OrderHoldingSerializer(ModelSerializer):
    class Meta:
        model = OrderHolding
        fields = ("id", "order_id", "printholo_cost", "fulfillment_cost", "create_time", "update_time")