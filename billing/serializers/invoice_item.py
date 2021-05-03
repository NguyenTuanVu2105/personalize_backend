from rest_framework.serializers import ModelSerializer

from billing.models import InvoiceItem
from order.serializers import OrderItemSerializer


class InvoiceItemSerializer(ModelSerializer):
    order_item = OrderItemSerializer()

    class Meta:
        model = InvoiceItem
        fields = ('order_item', 'quantity', 'price', 'currency')
