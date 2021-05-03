import stripe
from stripe.error import StripeError

from .currency import convert_to_smallest_unit


def stripe_auto_charge(invoice, stripe_payment_method):
    success = False
    amount = invoice.total_cost
    currency = invoice.currency
    metadata = {
        "invoice_id": invoice.id
    }

    try:
        charge = stripe.Charge.create(
            idempotency_key=invoice.idempotency_key,
            amount=convert_to_smallest_unit(amount, currency),
            currency=currency,
            customer=stripe_payment_method.customer_code,
            receipt_email=invoice.customer.email or None,
            metadata=metadata
        )

    except StripeError as e:
        detail = e.json_body
    except Exception as e:
        print("Stripe charge error: " + str(e))
        detail = {"message": str(e)}
    else:
        detail = charge
        success = True

    return success, detail
