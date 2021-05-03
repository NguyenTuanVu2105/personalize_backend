import logging

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from billing.sub_apps.combine_payment.functions import reorder_payment_methods
from billing.sub_apps.combine_payment.functions.general_payment_method import deactivate_payment_method
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod
from billing.sub_apps.combine_payment.serializers import GeneralPaymentMethodSerializer

logger = logging.getLogger(__name__)


class GeneralMethodViewSet(ModelViewSet):
    queryset = GeneralPaymentMethod.objects.active()
    serializer_class = GeneralPaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.by_user(self.request.user.pk)

    def destroy(self, request, *args, **kwargs):
        payment_method = self.get_object()
        deactivate_payment_method(payment_method)
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="reorder")
    def reorder_payment_method(self, request):
        new_payment_method_order = request.data.get("new_payment_method_order")
        payment_methods = self.get_queryset()
        payment_method_ids = [pm.id for pm in payment_methods]
        if len(payment_method_ids) != len(new_payment_method_order) \
                or set(payment_method_ids) - set(new_payment_method_order):
            return Response({"errors": ["Invalid payment method ids"]})
        reorder_payment_methods(new_payment_method_order, payment_methods)
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="test_refund")
    def test_refund(self, request):
        # auto_charging()
        # auto_refund()
        return Response({"success": True})
