import logging
import uuid

import requests
import simplejson
from django.core.exceptions import ValidationError
from django.utils import timezone

from billing.exceptions.payment_gateway_request_exception import RetryablePaymentRequestException, \
    UnretryablePaymentRequestException
from billing.models import Invoice
from service_communication.constants.request_type import RequestType
from service_communication.services.service_communication_log import create_service_communication_log_async, \
    extract_invoice_id_from_payload
from .paypal_authorization_services import PaypalAuthorizationService

logger = logging.getLogger(__name__)


class PaypalRequestService:
    @classmethod
    def post(cls, **kwargs):
        return cls.make_request(method="POST", **kwargs)

    @classmethod
    def get(cls, **kwargs):
        return cls.make_request(method="GET", **kwargs)

    @classmethod
    def delete(cls, **kwargs):
        return cls.make_request(method="DELETE", **kwargs)

    @classmethod
    def make_request(cls, method, url, data=None, headers=None, idempotency_key=None):
        access_token = PaypalAuthorizationService.get_access_token()
        if not access_token:
            raise ValidationError("Paypal access token is none")
        if not isinstance(headers, dict):
            headers = {}
        if not isinstance(idempotency_key, str):
            idempotency_key = str(uuid.uuid4())

        if method == "POST":
            json = data
            params = None
        else:
            json = None
            params = data

        headers["Authorization"] = f"Bearer {access_token}"
        headers["PayPal-Request-Id"] = idempotency_key
        status_code = -1
        text_response = ""
        request_time = timezone.now()
        try:
            response = requests.request(method=method, url=url, json=json, params=params, headers=headers, timeout=30)
            status_code = response.status_code
            text_response = response.text
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code_str = str(status_code)
            if status_code_str.startswith("4"):
                if status_code_str in ['401', '403']:
                    PaypalAuthorizationService.reset_token_and_renew_from_db()
                raise UnretryablePaymentRequestException(e)
            else:
                raise RetryablePaymentRequestException(e)
        except requests.RequestException as e:
            logger.error(e)
            raise RetryablePaymentRequestException(e)
        except simplejson.errors.JSONDecodeError:
            status_code = -1
            return {}
        finally:
            invoice_id = extract_invoice_id_from_payload(json)
            try:
                invoice = Invoice.objects.get(pk=invoice_id)
            except Invoice.DoesNotExist:
                invoice = None
            create_service_communication_log_async(request_type=RequestType.PAYMENT_PAYPAL_REQUEST,
                                                   status_code=status_code,
                                                   related_object=invoice,
                                                   response_body_as_text=text_response,
                                                   request_time=request_time,
                                                   response_time=timezone.now(),
                                                   payload=json)



