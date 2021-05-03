from rest_framework import serializers

from billing.sub_apps.combine_payment.models import GeneralPaymentMethod


class PartnerPaymentMethodSerializer(serializers.Serializer):
    email = serializers.EmailField()


class GeneralPaymentMethodSerializer(serializers.ModelSerializer):
    partner_payment_method = serializers.JSONField(source="payment_gateway_method_data")

    class Meta:
        model = GeneralPaymentMethod
        fields = ('id', 'partner_payment_method', 'ordinal_number', 'update_time')
