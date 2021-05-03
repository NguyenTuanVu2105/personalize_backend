import logging
import re

from HUB import settings
from .paypal_endpoint_service import PaypalEndpointService
from .paypal_request_services import PaypalRequestService

PRODUCT_VENDOR_NAME = settings.PRODUCT_VENDOR_NAME or ""

logger = logging.getLogger(__name__)


class PaypalBillingAgreementService:
    @staticmethod
    def create():
        response_json = PaypalRequestService.post(url=PaypalEndpointService.CREATE_BILLING_AGREEMENT_ENDPOINT,
                                                  data={
                                                      "name": "{} Billing Agreement".format(PRODUCT_VENDOR_NAME),
                                                      "payer": {
                                                          "payment_method": "PAYPAL"
                                                      },
                                                      "plan": {
                                                          "type": "MERCHANT_INITIATED_BILLING",
                                                          "merchant_preferences": {
                                                              "return_url": "https://.com/return",
                                                              "cancel_url": "https://.com/cancel",
                                                              "accepted_pymt_type": "INSTANT",
                                                              "skip_shipping_address": True,
                                                              "immutable_shipping_address": True
                                                          }
                                                      }
                                                  })

        links = response_json.get("links")
        if links:
            for link in links:
                if link.get("rel") == "approval_url":
                    href = link.get("href")
                    try:
                        agreement_token = re.search("BA-\w+", href).group()
                    except Exception as e:
                        return ""
                    else:
                        return agreement_token

    @staticmethod
    def activate(agreement_token):
        success = False
        if agreement_token and isinstance(agreement_token, str):
            response_json = PaypalRequestService.post(
                url=PaypalEndpointService.ACTIVATE_BILLING_AGREEMENT_ENDPOINT,
                data={
                    "token_id": agreement_token
                })
            agreement_id = response_json.get("id")
            payer_info = response_json.get("payer", {}).get("payer_info")
            if agreement_id and payer_info:
                success = True
                return success, agreement_id, payer_info
        return success, None, None

    @staticmethod
    def deactivate(agreement_id):
        success = False
        if agreement_id and isinstance(agreement_id, str):
            PaypalRequestService.post(
                url=PaypalEndpointService.CANCEL_BILLING_AGREEMENT_ENDPOINT.format(agreement_id=agreement_id),
                data={})
            success = True
        return success
