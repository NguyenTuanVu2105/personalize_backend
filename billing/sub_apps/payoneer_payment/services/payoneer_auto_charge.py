from billing.sub_apps.payoneer_payment.services.payoneer_sdk import PayoneerService


def payoneer_auto_charge(invoice, payoneer_payment_method, idempotency_key):
    charge_status, detail = PayoneerService.charge(payoneer_payment_method.payee_id,
                                                   invoice.total_cost,
                                                   idempotency_key,
                                                   invoice)
    detail = {
        "id": idempotency_key,
        "description": detail,
        "payee_id": payoneer_payment_method.payee_id
    }
    return charge_status, detail


def payoneer_get_transaction_id(transaction_detail):
    return transaction_detail.get("id")
