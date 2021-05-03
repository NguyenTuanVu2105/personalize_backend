from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from billing.constants.refund_statuses import REFUND_STATUSES, RefundStatus
from billing.constants.transaction_statuses import TransactionStatus
from billing.models import Refund, Transaction
from user.serializers.user import BriefUserSerializer


class RefundSerializer(ModelSerializer):
    status = CharField(source="verbose_status")

    class Meta:
        model = Refund
        fields = (
            "id", "refund_type", "description", "is_retryable", "is_approvable", "invoice_id", "amount", "currency",
            "status", "update_time", "info")


class AdminRefundSerializer(ModelSerializer):
    status = CharField(source="verbose_status")
    refund_type = CharField(source="verbose_refund_type")
    user = BriefUserSerializer()
    object_type = CharField(source="content_type_label")
    real_amount = SerializerMethodField()

    def get_real_amount(self, obj):
        content_type = ContentType.objects.filter(model="refund").first()
        transaction = Transaction.objects.filter(content_type=content_type, object_id=obj.id, status=TransactionStatus.SUCCESS).first()
        if transaction:
            if "amount" in transaction.detail:
                return transaction.detail["amount"]
        return {}

    class Meta:
        model = Refund
        fields = (
        "id", "refund_type","object_id","object_type", "user", "invoice_id", "description", "is_retryable", "is_approvable", "amount", "currency",
        "status","create_time", "update_time", "info", "real_amount")
