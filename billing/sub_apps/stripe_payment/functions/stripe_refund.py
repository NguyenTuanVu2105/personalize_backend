import stripe

from .currency import convert_to_smallest_unit


def stripe_refund(transaction_log, amount):
    is_success = False
    try:
        refund = stripe.Refund.create(
            charge=transaction_log.get("id"),
            amount=convert_to_smallest_unit(amount),
        )
    except stripe.error.CardError as e:
        detail = e.json_body
    except Exception as e:
        print("Stripe refund error: " + str(e))
        detail = {"message": str(e)}
    else:
        detail = refund
        is_success = True

    return is_success, detail
