from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from billing.sub_apps.paypal_vault_payment.services.paypal_order_services import PaypalOrderService


class PaypalOrderViewSet(AuthenticatedGenericViewSet):
    @action(methods=["POST"], detail=True, url_path="capture")
    def capture_order(self, request, *args, **kwargs):
        paypal_order_id = kwargs.pop("pk")
        success = False
        if paypal_order_id.strip():
            success = PaypalOrderService.capture_order(paypal_order_id)
        return Response({"success": success})


