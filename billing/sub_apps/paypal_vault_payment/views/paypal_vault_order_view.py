from rest_framework.response import Response

from HUB.views import AuthenticatedAPIView
from billing.sub_apps.combine_payment.functions.check_max_payment_method import check_max_user_payment_method
from billing.sub_apps.paypal_vault_payment.models import PaypalVaultPaymentMethod
from billing.sub_apps.paypal_vault_payment.services.paypal_order_services import PaypalOrderService
from billing.sub_apps.paypal_vault_payment.services.paypal_vault_payment_method_service import \
    PaypalVaultPaymentMethodService


class PaypalVaultOrderAPIView(AuthenticatedAPIView):

    def get(self, request):
        is_max_payment_method = check_max_user_payment_method(user=request.user, payment_model=PaypalVaultPaymentMethod)
        if is_max_payment_method:
            return Response({"success": False, "message": "The payment method exceeded allowed"})
        order_id = PaypalOrderService.create_order_for_authorize()
        return Response({"success": bool(order_id), "order_id": order_id})

    def post(self, request):
        user_id = request.user.id
        paypal_order_id = request.data.get("order_id", "")
        success = False
        is_max_payment_method = check_max_user_payment_method(user=request.user, payment_model=PaypalVaultPaymentMethod)
        if is_max_payment_method:
            return Response({"success": False, "message": "The payment method exceeded allowed"})
        if paypal_order_id.strip():
            # -- Capture order ---
            success = PaypalOrderService.capture_order(paypal_order_id)
            if not success:
                return Response({"success": False, "error": "CHARGE_FAILED"})
            # -- Check payment is in vaulted list
            success = PaypalVaultPaymentMethodService.check_payment_methods(user_id)
            if not success:
                return Response({"success": False, "error": "CHECK_FAILED"})
        return Response({"success": success})
