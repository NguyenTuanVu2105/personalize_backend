import logging

from billing.sub_apps.paypal_payment.services.paypal_endpoint_service import PaypalEndpointService
from billing.sub_apps.paypal_payment.services.paypal_request_services import PaypalRequestService

logger = logging.getLogger(__name__)


class PaypalVaultPaymentTokenService:
    @classmethod
    def list_payment_tokens_by_customer_id(cls, customer_id):
        response_json = PaypalRequestService.get(url=PaypalEndpointService.LIST_PAYMENT_TOKEN_BY_CUSTOMER_ID,
                                                 data={"customer_id": customer_id, "page_size": 10000,
                                                       "total_required": "true"})
        logger.info(response_json)
        if response_json.get("customer_id", "") and customer_id or response_json.get("total_pages") <= 1:
            return response_json.get("payment_tokens", [])

    @classmethod
    def get_payment_token_detail(cls, payment_token):
        response_json = PaypalRequestService.get(
            url=PaypalEndpointService.GET_PAYMENT_TOKEN_DETAIL.format(token_id=payment_token),
            data={})
        return response_json

    @classmethod
    def deactivate(cls, payment_token):
        response_json = PaypalRequestService.delete(
            url=PaypalEndpointService.GET_PAYMENT_TOKEN_DETAIL.format(token_id=payment_token),
            data={})
        return True
