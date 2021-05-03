import logging

from .paypal_endpoint_service import PaypalEndpointService
from .paypal_request_services import PaypalRequestService

logger = logging.getLogger(__name__)


class PaypalCustomerService:
    @classmethod
    def get_customer_token(cls, customer_id):
        response_json = PaypalRequestService.post(url=PaypalEndpointService.GENERATE_CUSTOMER_TOKEN,
                                                  data={
                                                      "customer_id": customer_id,
                                                  })

        customer_token = response_json.get("client_token", "")
        if not customer_token.strip():
            logger.error("Can't get customer [{}] - Response\n{}".format(customer_id, response_json))
            return
        return customer_token
