import jwt
import stripe
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.response import Response

from HUB.functions import get_token_from_request
from HUB.views import AuthenticatedAPIView
from billing.constants.invoice_statuses import InvoiceStatus
from billing.models import Invoice
from ..forms import CheckoutForm
from ..models import UserStripe

User = get_user_model()


class CheckoutView(AuthenticatedAPIView):
    error_messages = {
        "user_stripe": {
            "invalid": "This user_stripe is invalid",
        },
        "invoice": {
            "invalid": "This invoice is invalid",
            "charged": "This invoice have been charged"
        }
    }

    def post(self, request):
        request_data = request.data
        checkout_form = CheckoutForm(data=request_data)
        if checkout_form.is_valid():
            try:
                with transaction.atomic():
                    token = get_token_from_request(request)
                    # print(token)
                    seller_id = jwt.decode(token, None, None)['user_id']

                    type = request_data['type']
                    card_id = request_data['id']
                    amount = request_data['total_cost']
                    currency = request_data['currency']
                    metadata = request_data['metadata']
                    stripe_user = UserStripe.objects.get(id=card_id)
                    seller = User.objects.get(id=seller_id)
                    invoice_id = metadata['invoice_id']
                    invoice = Invoice.objects.get(id=invoice_id)
                    if invoice.status == InvoiceStatus.PAID:
                        return self.json_error(field='invoice', code="charged", status=200)
                    else:
                        charge = stripe.Charge.create(
                            amount=amount,
                            currency=currency,
                            customer=stripe_user.customer_code,
                            receipt_email=seller.email or None,
                            metadata=metadata
                        )

            except User.DoesNotExist:
                return self.json_error(field='user', code="invalid", status=200)

            except UserStripe.DoesNotExist:
                return self.json_error(field='user_stripe', code="invalid", status=200)

            except stripe.error.CardError as e:
                return Response({"success": False, "message": str(e)})

                # # Since it's a decline, stripe.error.CardError will be caught
                # body = e.json_body
                # err = body.get('error', {})
                #
                # print
                # "Status is: %s" % e.http_status
                # print
                # "Type is: %s" % err.get('type')
                # print
                # "Code is: %s" % err.get('code')
                # # param is '' in this case
                # print
                # "Param is: %s" % err.get('param')
                # print
                # "Message is: %s" % err.get('message')
            except stripe.error.RateLimitError as e:
                return Response({"success": False, "message": str(e)}, status=200)
                # Too many requests made to the API too quickly
                # pass
            except stripe.error.InvalidRequestError as e:
                return Response({"success": False, "message": str(e)}, status=200)
                # Invalid parameters were supplied to Stripe's API
                # pass
            except stripe.error.AuthenticationError as e:
                return Response({"success": False, "message": str(e)}, status=200)
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                # pass
            except stripe.error.APIConnectionError as e:
                return Response({"success": False, "message": str(e)}, status=200)
                # Network communication with Stripe failed
                # pass
            except stripe.error.StripeError as e:
                return Response({"success": False, "message": str(e)}, status=200)
                # Display a very generic error to the user, and maybe send
                # yourself an email
                # pass
            except Exception as e:
                return Response({"success": False, "message": str(e)}, status=200)

            else:
                return Response(
                    {"success": True, "message": "The card has been successfully charged", "data": request_data},
                    status=200)

        else:
            return Response(ValidationError(code="checkout", message=checkout_form.errors), status=200)
