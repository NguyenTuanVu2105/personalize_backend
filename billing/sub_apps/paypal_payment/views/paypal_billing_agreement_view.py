from rest_framework.response import Response

from HUB.views import AuthenticatedAPIView
from billing.sub_apps.combine_payment.functions.check_max_payment_method import check_max_user_payment_method
from billing.sub_apps.paypal_payment.models import PaypalPaymentMethod
from billing.sub_apps.paypal_payment.services import PaypalBillingAgreementService


class PaypalBillingAgreementAPIView(AuthenticatedAPIView):
    def post(self, request):
        agreement_token = PaypalBillingAgreementService.create()
        is_max_payment_method = check_max_user_payment_method(user=request.user, payment_model=PaypalPaymentMethod)
        if is_max_payment_method:
            return Response({"success": False, "message": "The payment method exceeded allowed"})
        return Response({"success": bool(agreement_token), "agreement_token": agreement_token})
