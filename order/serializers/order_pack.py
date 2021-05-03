from django.contrib.contenttypes.models import ContentType
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField

from billing.constants.transaction_statuses import TransactionStatus
from billing.models import InvoicePack, InvoiceItem, Refund, Invoice, Transaction
from order.models import OrderPack
from shop.serializers import ShopSerializer
from .fulfillment_order_pack import MerchantServiceFulfillmentOrderPackTrackingSerializer
from .order_cancel_shipping_request import BriefCancelShippingRequestSerializer
from .order_item import OrderItemSerializer, MerchantServiceOrderItemSerializer


class BriefOrderPackSerializer(ModelSerializer):
    fulfill_status = CharField(source="verbose_fulfill_status")

    class Meta:
        model = OrderPack
        fields = (
            "id", "fulfill_status", "service", "shipping_cost", "currency", "location_id", "order_id")


class OrderPackSerializer(BriefOrderPackSerializer):
    financial_status = CharField(source="verbose_financial_status")
    items = OrderItemSerializer(many=True)
    tracking_info = MerchantServiceFulfillmentOrderPackTrackingSerializer(many=True, source="fulfillment_order_packs")
    cancel_shipping_requests = BriefCancelShippingRequestSerializer(many=True)

    class Meta(BriefOrderPackSerializer.Meta):
        fields = (
            "id", "fulfill_status", "financial_status", "service", "tracking_info", "cancel_shipping_requests",
            "production_cost", "shipping_cost", "discount", "total_cost", "currency", "location_id", "items")


class MerchantServiceOrderPackSerializer(OrderPackSerializer):
    items = MerchantServiceOrderItemSerializer(many=True)


class MerchantServicePackTrackingSerializer(OrderPackSerializer):
    id = CharField(source="merch_pack_id")
    tracking_info = MerchantServiceFulfillmentOrderPackTrackingSerializer(many=True, source="fulfillment_order_packs")

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        tracking_info = representation.pop('tracking_info')
        joined_tracking_number = ", ".join(
            [item["tracking_number"] for item in tracking_info if item["tracking_number"]])
        representation["tracking_number"] = joined_tracking_number
        return representation

    class Meta(OrderPackSerializer.Meta):
        fields = ("id", "tracking_info")


class BriefInvoiceItemSerializer(ModelSerializer):
    order_item = OrderItemSerializer()

    class Meta:
        model = InvoiceItem
        fields = ('id', 'order_item', 'quantity', 'price', 'currency')


class BriefRefundSerializer(ModelSerializer):
    status = CharField(source="verbose_status")
    real_amount = SerializerMethodField()

    def get_real_amount(self, obj):
        content_type = ContentType.objects.filter(model="refund").first()
        transaction = Transaction.objects.filter(content_type=content_type, object_id=obj.id,
                                                 status=TransactionStatus.SUCCESS).first()
        if transaction:
            if "amount" in transaction.detail:
                return transaction.detail["amount"]
        return {}

    class Meta:
        model = Refund
        fields = (
            "id", "refund_type", "description", "is_retryable", "is_approvable", "invoice_id", "amount", "currency",
            "status", "update_time", "info", "real_amount")


class BriefInvoiceSerializer(ModelSerializer):
    refund_history = BriefRefundSerializer(source="refunds", many=True)

    class Meta:
        model = Invoice
        fields = (
            'id', 'refund_history')


class BriefInvoicePackSerializer(ModelSerializer):
    shop = ShopSerializer()
    items = BriefInvoiceItemSerializer(many=True)
    invoice = BriefInvoiceSerializer()

    class Meta:
        model = InvoicePack
        fields = ('id', 'invoice_id', 'shop', 'items', 'status', 'production_cost', 'shipping_cost', 'discount', 'tax',
                  'total_cost', 'currency', 'invoice')


class OrderPackWithInvoicesSerializer(OrderPackSerializer):
    invoice_pack = BriefInvoicePackSerializer()

    class Meta(OrderPackSerializer.Meta):
        fields = OrderPackSerializer.Meta.fields + ('invoice_pack',)
