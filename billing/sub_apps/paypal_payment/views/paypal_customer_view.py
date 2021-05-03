from rest_framework.response import Response
from django.core.cache import cache
from HUB.views import AuthenticatedAPIView
from billing.sub_apps.paypal_payment.services.paypal_authorization_services import PaypalAuthorizationService
from billing.sub_apps.paypal_payment.services.paypal_customer_services import PaypalCustomerService


class PaypalCustomerAPIView(AuthenticatedAPIView):

    def get(self, request):
        customer_id = request.user.id
        key = "PaypalCustomerAPIView__token_{}".format(customer_id)
        customer_token = cache.get(key)
        if not customer_token:
            customer_token = PaypalCustomerService.get_customer_token(customer_id)
            cache.set(key, customer_token, 60 * 60 - 10)
        return Response({"success": bool(customer_token), "client_id": PaypalAuthorizationService.get_client_id(), "customer_token": customer_token})
