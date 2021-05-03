from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from billing.sub_apps.braintree_payment.braintree_service import braintree_gateway
from billing.sub_apps.braintree_payment.models import BraintreePaymentMethod
from billing.sub_apps.braintree_payment.serializers import PaymentMethodSerializer
from helper.string_helpers import convert_camel_to_underscore


class PaymentMethodViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           AuthenticatedGenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BraintreePaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        user = request.user
        customer = braintree_gateway.customer.find(customer_id=str(user.pk))
        payment_methods = customer.payment_methods
        for payment_method in payment_methods:
            BraintreePaymentMethod.objects.update_or_create(user_id=payment_method.customer_id,
                                                            email=payment_method.email,
                                                            type=convert_camel_to_underscore(
                                                                payment_method.__class__.__name__),
                                                            token=payment_method.token)
        return Response({"success": True})
