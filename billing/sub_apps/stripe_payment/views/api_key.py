from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from HUB.views import AuthenticatedAPIView

User = get_user_model()

public_key = settings.STRIPE_PK_KEY


class StripeAPIKeyView(AuthenticatedAPIView):
    def get(self, request):
        return Response({"api_key": public_key})
