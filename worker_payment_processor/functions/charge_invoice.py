import logging

from django.db import transaction

from HUB import settings
from billing.constants.transaction_statuses import TransactionStatus
from billing.constants.transaction_types import TransactionType
from billing.exceptions.payment_gateway_request_exception import UnretryablePaymentRequestException, \
    RetryablePaymentRequestException
from billing.sub_apps.combine_payment.constants import PaymentGateway
from billing.sub_apps.payoneer_payment.services.payoneer_auto_charge import payoneer_auto_charge
from billing.sub_apps.paypal_payment.services import paypal_auto_charge
from billing.sub_apps.paypal_vault_payment.services import paypal_vault_auto_charge
from helper.string_helpers import hash_str_to_uuid

logger = logging.getLogger(__name__)


@transaction.atomic
def charge_invoice(payment_processor_info):
    invoice_obj = payment_processor_info.invoice
    charge_status = TransactionStatus.CHARGE_FAILED
    transactions = []

    is_valid = validate_invoice(invoice_obj)
    if is_valid:
        for payment_method in payment_processor_info.payment_methods.all():
            idempotency_key = get_payment_method_idempotency_key(payment_processor_info, payment_method)
            try:
                charge_status, detail = charge_payment_gateway_method(payment_processor_info, payment_method,
                                                                      idempotency_key)
            except UnretryablePaymentRequestException as e:
                logger.error(e)
                continue
            except RetryablePaymentRequestException as e:
                charge_status = TransactionStatus.TRANSACTION_PENDING
                detail = {"error": str(e)}
            transaction_info = {
                "content_object": invoice_obj,
                "type": TransactionType.CHARGE,
                "payment_method": payment_method.id,
                "status": charge_status,
                "detail": detail,
                "idempotency_key": idempotency_key
            }
            transactions.append(transaction_info)

            stop = should_stop_charging(charge_status, invoice_obj, payment_method)
            if stop:
                break
    else:
        charge_status = TransactionStatus.CANCELED

    return charge_status, transactions


def validate_invoice(invoice_obj):
    if invoice_obj.total_cost <= 0:
        return False
    return True


def charge_payment_gateway_method(payment_processor_info, payment_method, idempotency_key):
    invoice = payment_processor_info.invoice
    payment_gateway_method = payment_method.content_object
    payment_gateway = payment_gateway_method.gateway_name

    if payment_gateway == PaymentGateway.PAYONEER:
        return payoneer_auto_charge(invoice, payment_gateway_method, idempotency_key)
    elif payment_gateway == PaymentGateway.PAYPAL_PRO:
        return paypal_auto_charge(invoice, payment_gateway_method, idempotency_key)
    elif payment_gateway == PaymentGateway.PAYPAL_VAULT:
        return paypal_vault_auto_charge(invoice, payment_gateway_method, idempotency_key)
    else:
        logger.error("Unknown payment gateway - Gateway: {}".format(payment_gateway))
        raise UnretryablePaymentRequestException


def should_stop_charging(charge_status, invoice, payment_method):
    if charge_status == TransactionStatus.SUCCESS:
        # Has nothing to say
        logger.info("CHARGE_SUCCESSFULLY - Invoice {} - Payment method: {}".format(invoice.id, payment_method))
        return True
    elif charge_status == TransactionStatus.TRANSACTION_PENDING:
        # Do nothing util know transaction failed or not, so return immediately and comeback at next charge
        logger.info("TRANSACTION_PENDING - Invoice {} - Payment method: {}".format(invoice.id, payment_method))
        return True
    elif charge_status == TransactionStatus.TRANSACTION_FAILED:
        # charge succeed but transaction failed, cannot reuse current idempotency_key, set None to renew it
        logger.warning("TRANSACTION_FAILED - Invoice {} - Payment method: {}".format(invoice.id, payment_method))
        return False

    elif charge_status == TransactionStatus.CHARGE_FAILED:
        # charge failed (due to low balance or error), will try another methods or next charge, no need to renew idempotency_key
        logger.warning("CHARGE_FAILED - Invoice {} - Payment method: {}".format(invoice.id, payment_method))
        return False
    return False


def get_payment_method_idempotency_key(payment_processor_info, payment_method):
    raw_key = f'{settings.IDEMPOTENCY_KEY_PREFIX}{payment_processor_info.id}_{payment_method.id}'
    hash_key = hash_str_to_uuid(raw_key)
    logger.info(f'Idempotency_key: Raw = [{raw_key}], Hash = [{hash_key}]')
    return hash_key
