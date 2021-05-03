from rest_framework.response import Response

from HUB.views import AuthenticatedAPIView


class PaypalVaultTestView(AuthenticatedAPIView):

    def get(self, request):
        return Response({"success": False})
