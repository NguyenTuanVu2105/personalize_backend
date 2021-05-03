import logging

from billing.functions.get_idempotency_key import get_idempotency_key
from billing.sub_apps.paypal_payment.services.paypal_endpoint_service import PaypalEndpointService
from billing.sub_apps.paypal_payment.services.paypal_request_services import PaypalRequestService

logger = logging.getLogger(__name__)


class PaypalRefundOrderService:
    @staticmethod
    def refund(refund_id, capture_id, amount):
        response_json = PaypalRequestService.post(
            url=PaypalEndpointService.REFUND_ORDER_ENDPOINT.format(capture_id=capture_id),
            data={
                "amount": {
                    "value": amount,
                    "currency_code": "USD",
                },
                "note_to_payer": f'Refund #{refund_id}',
                "invoice_id": get_idempotency_key(refund_id)
            })
        success = bool(response_json.get("id"))
        return success, response_json


def paypal_auto_refund_order(refund_id, payment_gateway_transaction_id, amount):
    if not payment_gateway_transaction_id:
        logger.error("Invalid payment_gateway_transaction_id in sale transaction log [Refund {}]".format(refund_id))
        return
    is_success, detail = PaypalRefundOrderService.refund(refund_id=refund_id, capture_id=payment_gateway_transaction_id, amount=amount)
    return is_success, detail
