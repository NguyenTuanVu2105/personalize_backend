import logging

from django.db import transaction

from billing.constants.transaction_statuses import TransactionStatus
from billing.exceptions.payment_gateway_request_exception import UnretryablePaymentRequestException
from billing.models import Refund, Invoice
from billing.services import save_new_refund_transaction
from billing.sub_apps.braintree_payment.services import braintree_refund
from billing.sub_apps.combine_payment.constants import PaymentGateway
from billing.sub_apps.payoneer_payment.services.payoneer_refund import payoneer_refund
from billing.sub_apps.paypal_payment.services import paypal_auto_refund_sale
from billing.sub_apps.paypal_vault_payment.services import paypal_auto_refund_order
from billing.sub_apps.stripe_payment.functions import stripe_refund
from notification.enums.message_types import MessageType
from notification.services.notification import send_admin_notification

logger = logging.getLogger(__name__)


@transaction.atomic
def auto_refund():
    refunds = Refund.objects.pending()
    for refund_obj in refunds:
        send_refund(refund_obj)


def send_refund(refund_obj):
    invoice = Invoice.objects.filter(pk=refund_obj.invoice_id).first()
    payment_gateway, payment_method, payment_gateway_transaction_id, transaction_log = invoice.get_success_payment_info()

    if not transaction_log:
        logger.error("Can't find success transaction log for invoice {}".format(invoice.pk))
        refund_obj.set_failed()
        return

    amount = refund_obj.amount
    try:
        if payment_gateway == PaymentGateway.PAYONEER:
            payee_id = transaction_log.get("payee_id")
            is_success, detail = payoneer_refund(refund_id=refund_obj.id,
                                                 payee_id=payee_id,
                                                 amount=amount)
        elif payment_gateway == PaymentGateway.PAYPAL_PRO:
            is_success, detail = paypal_auto_refund_sale(refund_id=refund_obj.pk,
                                                         payment_gateway_transaction_id=payment_gateway_transaction_id,
                                                         amount=amount)
        elif payment_gateway == PaymentGateway.PAYPAL_VAULT:
            is_success, detail = paypal_auto_refund_order(refund_id=refund_obj.pk,
                                                          payment_gateway_transaction_id=payment_gateway_transaction_id,
                                                          amount=amount)
        else:
            logger.warning("Unknown payment method while refunding - {}".format(payment_gateway))
            return
    except UnretryablePaymentRequestException:
        is_success = False
    else:
        transaction_id = save_new_refund_transaction(payment_method=payment_method,
                                                     data={"content_object": refund_obj,
                                                           "status": TransactionStatus.SUCCESS if is_success else TransactionStatus.TRANSACTION_FAILED,
                                                           "detail": detail,
                                                           "payment_gateway": payment_gateway})
        if is_success:
            refund_obj.set_settled()
            logger.info("Refund succeed - Traceback auto refund transaction: {}".format(transaction_id))
            return

    refund_obj.set_failed()
    data = {
        "refund_id": refund_obj.id,
        "invoice_id": refund_obj.invoice_id,
        "amount": amount
    }
    send_admin_notification.delay(MessageType.ADMIN_REFUND_FAILED, data)
    logger.warning("Refund failed - Traceback auto refund ID: {}".format(refund_obj.id))
