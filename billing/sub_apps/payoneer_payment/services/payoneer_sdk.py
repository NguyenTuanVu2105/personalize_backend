import base64
import logging

import requests
from django.utils import timezone

from HUB import settings
from billing.constants.transaction_statuses import TransactionStatus
from billing.exceptions.payment_gateway_request_exception import UnretryablePaymentRequestException, \
    RetryablePaymentRequestException
from service_communication.constants.request_type import RequestType
from service_communication.services.service_communication_log import create_service_communication_log_async

logger = logging.getLogger(__name__)


class PayoneerService:
    AUTHORIZATION_USER = settings.PAYONEER_USERNAME
    AUTHORIZATION_PASSWORD = settings.PAYONEER_PASSWORD
    PROGRAM_ID = settings.PAYONEER_PROGRAM_ID
    HOST = settings.PAYONEER_HOST
    AUTHORIZATION_BASIC_AUTH = AUTHORIZATION_USER + ':' + AUTHORIZATION_PASSWORD
    AUTHORIZATION_HEADER = 'Basic ' + base64.b64encode(AUTHORIZATION_BASIC_AUTH.encode("utf-8")).decode("utf-8")
    ENDPOINTS = {
        'charge': f'{HOST}/v2/programs/{PROGRAM_ID}/charges',
        'get_charge_status': f'{HOST}/v2/programs/{PROGRAM_ID}/charges/{{}}/status',
        'refund': f'{HOST}/v2/programs/{PROGRAM_ID}/payouts',
        'create_login_link': f'{HOST}/v2/programs/{PROGRAM_ID}/payees/login-link',
        'get_payee_status': f'{HOST}/v2/programs/{PROGRAM_ID}/payees/{{}}/status',
        'get_payee_details': f'{HOST}/v2/programs/{PROGRAM_ID}/payees/{{}}/details',
        'delete_payee': f'{HOST}/v2/programs/{PROGRAM_ID}/payees/{{}}',
    }
    LOGIN_REDIRECT_URL = f'{settings.PAYONEER_LOGIN_REDIRECT_URL}'
    HEADERS = {'authorization': AUTHORIZATION_HEADER}

    @classmethod
    def charge(cls, payee_id, amount, idempotency_key, invoice):
        invoice_id = invoice.payment_gateway_invoice_id
        payload = {
            "payee_id": payee_id,
            "amount": amount,
            "client_reference_id": idempotency_key,
            "description": f"Invoice {invoice_id}",
            "currency": settings.BASE_CURRENCY
        }
        status_code = -1
        request_time = timezone.now()
        res_data_text = ""
        try:
            response = requests.request("POST", cls.ENDPOINTS['charge'], json=payload, headers=cls.HEADERS)
            status_code = response.status_code
            res_data_text = response.text
            res_data = response.json()
        except requests.exceptions.HTTPError as e:
            status_code_str = str(status_code)
            if status_code_str.startswith("4"):
                raise UnretryablePaymentRequestException(e)
            else:
                raise RetryablePaymentRequestException(e)
        except requests.RequestException as e:
            logger.error(e)
            raise RetryablePaymentRequestException(e)
        finally:
            create_service_communication_log_async(request_type=RequestType.PAYMENT_PAYONEER_CHARGE,
                                                   status_code=status_code,
                                                   related_object=invoice,
                                                   response_body_as_text=res_data_text,
                                                   request_time=request_time,
                                                   response_time=timezone.now(),
                                                   payload=payload)
        logger.info(res_data)
        res_code = res_data.get("code")
        # 0 = success, 10704 = Duplicated ClientRefId
        if res_code == 0 or res_code == 10704:
            return cls.check_charge_status(idempotency_key)
        else:
            return TransactionStatus.CHARGE_FAILED, res_data

    @classmethod
    def check_charge_status(cls, idempotency_key):
        try:
            res = requests.request("GET", cls.ENDPOINTS['get_charge_status'].format(idempotency_key),
                                   headers=cls.HEADERS)
            charge_status_data = res.json()
        except Exception as e:
            logger.exception(e)
            return TransactionStatus.TRANSACTION_PENDING, None
        logger.info(charge_status_data)
        if charge_status_data.get("code", 1) != 0 or "status" not in charge_status_data:
            return TransactionStatus.CHARGE_FAILED, charge_status_data
        charge_status = charge_status_data.get("status")
        if charge_status == 'Transferred':
            return TransactionStatus.SUCCESS, charge_status_data
        elif charge_status == 'Refunded':
            return TransactionStatus.TRANSACTION_FAILED, charge_status_data
        else:
            return TransactionStatus.TRANSACTION_PENDING, charge_status_data

    @classmethod
    def is_payee_active(cls, payee_id):
        res = requests.request("GET", cls.ENDPOINTS['get_payee_status'].format(payee_id), headers=cls.HEADERS)
        json = res.json()
        logger.info(json)
        return json.get("status", "INACTIVE") == 'ACTIVE'

    @classmethod
    def get_payee_detail(cls, payee_id):
        res = requests.request("GET", cls.ENDPOINTS['get_payee_details'].format(payee_id), headers=cls.HEADERS)
        json = res.json()
        logger.info(json)
        return json

    @classmethod
    def delete_payee(cls, payee_id):
        res = requests.request("DELETE", cls.ENDPOINTS['delete_payee'].format(payee_id), headers=cls.HEADERS)
        json = res.json()
        logger.info(json)
        return True

    @classmethod
    def refund(cls, payee_id, amount, idempotency_key, description):
        payload = {
            "payee_id": payee_id,
            "amount": amount,
            "client_reference_id": idempotency_key,
            "description": description,
            "currency": settings.BASE_CURRENCY
        }
        res = requests.request("POST", cls.ENDPOINTS['refund'], json=payload, headers=cls.HEADERS)
        json = res.json()
        logger.info(json)
        return json

    @classmethod
    def create_login_link(cls, payee_id, redirect_url):
        payload = {
            "payee_id": payee_id,
            "redirect_url": redirect_url,
            "redirect_time": "0",
        }
        logger.info(payload)
        logger.info(cls.HEADERS)
        res = requests.request("POST", cls.ENDPOINTS['create_login_link'], json=payload, headers=cls.HEADERS)
        json = res.json()
        logger.info(json)
        return json["login_link"]
