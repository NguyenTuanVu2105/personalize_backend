import logging

from billing.functions.get_idempotency_key import get_idempotency_key
from .paypal_endpoint_service import PaypalEndpointService
from .paypal_request_services import PaypalRequestService

logger = logging.getLogger(__name__)


class PaypalRefundSaleService:
    @staticmethod
    def refund(refund_id, sale_id, amount):
        response_json = PaypalRequestService.post(
            url=PaypalEndpointService.REFUND_SALE_ENDPOINT.format(sale_id=sale_id),
            data={
                "amount": {
                    "total": amount,
                    "currency": "USD",

                },
                "description": f'Refund #{refund_id}',
                "invoice_number": get_idempotency_key(refund_id)
            })
        success = bool(response_json.get("id"))
        return success, response_json


def paypal_auto_refund_sale(refund_id, payment_gateway_transaction_id, amount):
    if not payment_gateway_transaction_id:
        logger.error("Invalid payment_gateway_transaction_id in sale transaction log [Refund {}]".format(refund_id))
        return
    is_success, detail = PaypalRefundSaleService.refund(refund_id=refund_id, sale_id=payment_gateway_transaction_id,
                                                        amount=amount)
    return is_success, detail
