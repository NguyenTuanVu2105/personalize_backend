from billing.sub_apps.braintree_payment.braintree_service import braintree_gateway
from helper.encoders import JSONEncoder


def braintree_auto_charge(invoice, braintree_payment_method):
    result = braintree_gateway.transaction.sale({
        "customer_id": str(invoice.customer.id),
        "payment_method_token": braintree_payment_method.token,
        "order_id": invoice.idempotency_key,
        "amount": invoice.total_cost,
        "options": {
            "submit_for_settlement": True
        }
    })
    is_success = result.is_success
    if is_success:
        transaction = result.transaction
        detail = JSONEncoder().default(transaction)

    else:
        detail = {"error": result.message}

    return is_success, detail
