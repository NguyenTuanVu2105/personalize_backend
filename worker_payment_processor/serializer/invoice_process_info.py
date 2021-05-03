from rest_framework.serializers import ModelSerializer

from billing.sub_apps.combine_payment.serializers import GeneralPaymentMethodSerializer
from worker_payment_processor.models import InvoiceProcessInfo


class InvoiceProcessInfoSerializer(ModelSerializer):
    payment_methods = GeneralPaymentMethodSerializer(many=True)

    class Meta:
        model = InvoiceProcessInfo
        fields = ('id', 'invoice', 'idempotency_key', 'payment_methods', 'worker_host', 'create_time')
