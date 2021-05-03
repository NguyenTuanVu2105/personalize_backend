from billing.sub_apps.braintree_payment.braintree_service import braintree_gateway
from helper.encoders import JSONEncoder


def braintree_refund(transaction_log, amount):
    result = braintree_gateway.transaction.refund(transaction_log.get("id"), amount)
    is_success = result.is_success
    if is_success:
        transaction = result.transaction
        detail = JSONEncoder().default(transaction)
    else:
        detail = {"error": result.message}

    return result.is_success, detail
