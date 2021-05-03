import json
import logging
from datetime import timedelta

from django.db import transaction

from billing.constants.invoice_statuses import InvoiceStatus
from billing.constants.transaction_statuses import TransactionStatus, TRANSACTION_STATUS_DICT
from billing.constants.transaction_types import TransactionType
from billing.models import Invoice
from billing.serializers import TransactionSerializer
from billing.sub_apps.combine_payment.constants import PaymentGateway
from billing.sub_apps.payoneer_payment.services.payoneer_sdk import PayoneerService
from helper.datetime_helpers import get_current_datetime
from notification.enums.message_types import MessageType
from notification.services.notification import send_admin_notification
from worker_payment_processor.functions.charge_invoice import should_stop_charging, get_payment_method_idempotency_key
from worker_payment_processor.functions.check_invoice import get_invoice_processing_info_key
from worker_payment_processor.functions.update_invoice import update_invoice
from worker_payment_processor.models import InvoiceProcessInfo
from worker_payment_processor.serializer.invoice_process_info import InvoiceProcessInfoSerializer

logger = logging.getLogger(__name__)

DUE_TIME_PROCESSING_IN_MIN = 2 * 60


def auto_check_long_invoice_processing():
    due_time = get_current_datetime() - timedelta(minutes=DUE_TIME_PROCESSING_IN_MIN)
    long_processing_invoices = Invoice.objects.filter(status=InvoiceStatus.PROCESSING, update_time__lt=due_time)
    for invoice in long_processing_invoices:
        check_long_processing_charge(invoice)


@transaction.atomic
def check_long_processing_charge(invoice):
    current_invoice_processing_info = InvoiceProcessInfo.objects.get(
        pk=get_invoice_processing_info_key(invoice.id, invoice.charge_count))
    payment_methods = current_invoice_processing_info.payment_methods
    logger.info("Checking Invoice " + current_invoice_processing_info.id)
    charge_status = TransactionStatus.CHARGE_FAILED
    transactions = []
    for payment_method in payment_methods.all():
        payment_gateway_method = payment_method.content_object
        idempotency_key = get_payment_method_idempotency_key(current_invoice_processing_info, payment_method)
        charge_status, detail = check_gateway(payment_method, idempotency_key)
        if not charge_status:
            continue

        transaction_info = {
            "content_object": invoice,
            "type": TransactionType.CHARGE,
            "payment_method": payment_method.id,
            "status": charge_status,
            "detail": detail
        }
        transactions.append(transaction_info)
        stop = should_stop_charging(charge_status, invoice, payment_gateway_method)
        if stop:
            break

    # ---- UPDATE INVOICE ---
    try:
        invoice, saved_transactions = update_invoice(current_invoice_processing_info, charge_status, transactions)
        logger.info(saved_transactions)
        send_admin_notification(MessageType.ADMIN_LONG_INVOICE_PROCESSING, {
            "invoice_id": invoice.id,
            "data": json.dumps({
                "invoice": invoice.id,
                "invoice_processing_info": InvoiceProcessInfoSerializer(instance=current_invoice_processing_info).data,
                "transactions": TransactionSerializer(instance=saved_transactions, many=True).data,
                "charge_status": TRANSACTION_STATUS_DICT.get(charge_status)
            })

        })
    except Exception as e:
        logger.exception(e)


def check_gateway(payment_method, idempotency_key):
    payment_gateway_method = payment_method.content_object
    payment_gateway = payment_gateway_method.gateway_name
    if payment_gateway == PaymentGateway.STRIPE:
        # TODO update here when Stripe enable
        return TransactionStatus.CHARGE_FAILED, {}
    elif payment_gateway == PaymentGateway.BRAINTREE:
        # TODO update here when Braintree enable
        return TransactionStatus.CHARGE_FAILED, {}
    elif payment_gateway == PaymentGateway.PAYONEER:
        return PayoneerService.check_charge_status(idempotency_key)
    elif payment_gateway in PaymentGateway.PAYPAL_PRO:
        pass
        # return PaypalSaleService.get_payment_detail(idempotency_key)
    elif payment_gateway in PaymentGateway.PAYPAL_VAULT:
        pass
        # return PaypalOrderService.get_order_detail(idempotency_key)
    else:
        logger.error("Unknown payment gateway - Gateway: {}".format(payment_gateway))
        pass
    return None, None
