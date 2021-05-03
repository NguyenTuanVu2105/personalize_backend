import traceback

from billing.sub_apps.braintree_payment.braintree_service import braintree_gateway


def braintree_deactivate_payment_method(payment_method):
    try:
        result = braintree_gateway.payment_method.delete(payment_method.token)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
    else:
        if not result.is_success:
            print("Error while deactivating", result.message)

    return True
