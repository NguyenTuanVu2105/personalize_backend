from rest_framework.serializers import ModelSerializer, CharField

from billing.models import InvoicePack
from order.serializers import BriefOrderPackSerializer
from shop.serializers import ShopSerializer
from .invoice_item import InvoiceItemSerializer


class InvoicePackSerializer(ModelSerializer):
    shop = ShopSerializer()
    items = InvoiceItemSerializer(many=True)
    order_pack = BriefOrderPackSerializer()

    class Meta:
        model = InvoicePack
        fields = (
            'order_pack', 'shop', 'status', 'production_cost', 'shipping_cost', 'discount', 'tax', 'total_cost',
            'currency',
            "items")
