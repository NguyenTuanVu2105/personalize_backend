import traceback

import stripe


def stripe_deactivate_payment_method(payment_method):
    try:
        stripe.Customer.delete(payment_method.customer_code)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
    return True
