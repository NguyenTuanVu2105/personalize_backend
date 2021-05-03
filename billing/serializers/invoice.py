from rest_framework.serializers import ModelSerializer, CharField, JSONField

from billing.models import Invoice
from user.serializers import UserProfileSerializer
from .invoice_pack import InvoicePackSerializer
from .refund import RefundSerializer


class BriefInvoiceSerializer(ModelSerializer):
    total_cost = CharField(source="get_total_cost")
    currency = CharField()
    payment_method = JSONField(source="success_payment_method")

    class Meta:
        model = Invoice
        fields = ('id', 'total_cost', 'currency', 'status', 'create_time', 'update_time', 'paid_time', 'payment_method')


class InvoiceSerializer(BriefInvoiceSerializer):
    packs = InvoicePackSerializer(many=True)
    customer = UserProfileSerializer()
    refunds = RefundSerializer(many=True)

    class Meta(BriefInvoiceSerializer.Meta):
        fields = (
            'id', 'customer', 'total_cost', 'currency', 'status', 'packs', 'create_time', 'update_time', 'paid_time',
            'payment_method', "refunds")
