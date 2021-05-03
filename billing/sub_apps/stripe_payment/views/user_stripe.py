import stripe
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.response import Response

from HUB.views import AuthenticatedAPIView
from ..forms import UserStripeForm
from ..models import UserStripe

User = get_user_model()


class UserStripeListView(AuthenticatedAPIView):
    error_messages = {
        "user": {
            "invalid": "This user is invalid",
        }
    }

    def get(self, request):
        stripe_users = UserStripe.objects.filter(user_id=request.user.pk).order_by('billing_order')
        stripe_users_data = []
        for stripe_user in stripe_users:
            stripe_users_data.append(stripe_user.parse_info())
        return Response({"success": True, "data": stripe_users_data}, status=200)


class UserStripeCreateView(AuthenticatedAPIView):
    error_messages = {
        "user": {
            "invalid": "This user is invalid",
        }
    }

    def post(self, request):
        request_data = request.data
        user_stripe_form = UserStripeForm(data=request_data)
        if user_stripe_form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    token = request_data['token']
                    method = request_data['type']
                    card_name = request_data['name']

                    customer = stripe.Customer.create(
                        name=user.name or "",
                        source=token,
                        email=user.email or "",
                        address={"line1": user.address or ""},
                        phone=user.phone_number or "",
                    )
                    source = customer.sources.data[0]
                    UserStripe.objects.update_or_create(user=user, fingerprint=source.fingerprint,
                                                        customer_code=customer.id,
                                                        defaults={"type": method, "card_name": card_name,
                                                                  "last4": source.last4, "country": source.country,
                                                                  "exp_month": source.exp_month,
                                                                  "exp_year": source.exp_year})

            except User.DoesNotExist:
                return self.json_error(field='user', code="invalid")

            except Exception as e:
                return Response({"success": False, "message": str(e)})

            else:
                return Response({"success": True}, status=200)
        else:
            return Response(ValidationError(code="user_stripe", message=user_stripe_form.errors))
