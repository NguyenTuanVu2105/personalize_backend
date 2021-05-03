from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, CurrentUserDefault

from billing.sub_apps.braintree_payment.models import BraintreePaymentMethod


class PaymentMethodSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(
        read_only=True,
        default=CurrentUserDefault()
    )

    class Meta:
        model = BraintreePaymentMethod
        fields = ('user', "email", "token", "create_time", "update_time")

    def create(self, validated_data):
        email = validated_data.get('email')
        user = validated_data.get('user')
        payment_method = BraintreePaymentMethod.objects.filter(user=user, email=email).first()
        if not payment_method:
            payment_method = super().create(validated_data)
        return payment_method
