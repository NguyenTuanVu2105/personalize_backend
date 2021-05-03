from billing.functions.get_idempotency_key import get_idempotency_key
from billing.sub_apps.payoneer_payment.services.payoneer_sdk import PayoneerService


def payoneer_refund(refund_id, payee_id, amount):
    is_success = False

    try:
        refund = PayoneerService.refund(
            payee_id=payee_id,
            amount=amount,
            idempotency_key=f'{get_idempotency_key(refund_id)}_refund',
            description=f"Refund #{refund_id}"
        )
    except Exception as e:
        print("Payoneer refund error: " + str(e))
        detail = {"message": str(e)}
    else:
        detail = refund
        is_success = refund['code'] == 0

    return is_success, detail
