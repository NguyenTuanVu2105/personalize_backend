from rest_framework import status
from rest_framework.response import Response

from HUB.views import AuthenticatedAPIView


class PaypalAuthorizationAPIView(AuthenticatedAPIView):
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
