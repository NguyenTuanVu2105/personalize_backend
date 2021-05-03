from rest_framework.response import Response

from HUB.views import AuthenticatedAPIView
from billing.sub_apps.braintree_payment.braintree_service import braintree_gateway


class ClientTokenAPIView(AuthenticatedAPIView):

    def get(self, request):
        client_token = braintree_gateway.client_token.generate({
            "customer_id": request.user.pk
        })
        return Response({"client_token": client_token})
