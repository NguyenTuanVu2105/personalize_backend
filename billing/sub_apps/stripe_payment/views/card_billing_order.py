import jwt
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from HUB.functions import get_token_from_request
from HUB.views import AuthenticatedAPIView
from ..models import UserStripe

User = get_user_model()


class OrderCard(AuthenticatedAPIView):
    error_messages = {
        "card": {
            "invalid": "This card is invalid",
        }
    }

    def post(self, request):
        try:
            request_data = request.data
            cards = request_data['cards']
            token = get_token_from_request(request)
            seller_id = jwt.decode(token, None, None)['user_id']
            for index, card in enumerate(cards):
                stripe_user = UserStripe.objects.get(id=card['id'])
                stripe_user.billing_order = index + 1
                stripe_user.save()

        except UserStripe.DoesNotExist:
            return self.json_error(field='card', code="invalid")
        except Exception as e:
            return Response({"success": False, "message": str(e)})
        else:
            return Response({"success": True}, status=200)
