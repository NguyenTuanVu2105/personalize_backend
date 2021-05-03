import logging

from django.db import transaction

from billing.constants.transaction_statuses import TransactionStatus
from billing.forms.transaction import TransactionUpdateForm
from billing.models import Invoice
from billing.sub_apps.combine_payment.constants import PaymentGateway
from billing.sub_apps.combine_payment.functions.charge_result_handling import process_failed_charge, \
    process_success_charge, process_pending_charge
from billing.sub_apps.payoneer_payment.services.payoneer_sdk import PayoneerService
from billing.sub_apps.paypal_payment.services import paypal_auto_charge
from billing.sub_apps.paypal_vault_payment.services.paypal_order_services import PaypalOrderService, \
    paypal_vault_auto_charge
from billing.sub_apps.paypal_payment.services.paypal_sale_services import PaypalSaleService

logger = logging.getLogger(__name__)


class TransactionPendingChecker:
    @classmethod
    def auto_check_transaction_pending_invoice(cls):
        transaction_pending_invoices = Invoice.objects.transaction_pending()
        for invoice in transaction_pending_invoices:
            cls.check_transaction_pending_charge(invoice)

    @classmethod
    @transaction.atomic
    def check_transaction_pending_charge(cls, invoice):
        pending_transaction = invoice.transactions.pending().first()
        if not pending_transaction:
            return
        charge_status, transaction_info = cls.get_transaction_info_from_payment_gateway(invoice, pending_transaction)
        cls.handle_pending_charge_after_check(invoice, pending_transaction, charge_status, transaction_info)

    @classmethod
    def get_transaction_info_from_payment_gateway(cls, invoice, pending_transaction):
        payment_gateway = pending_transaction.payment_gateway
        payment_gateway_transaction_id = pending_transaction.payment_gateway_transaction_id
        idempotency_key = pending_transaction.idempotency_key
        payment_gateway_method = pending_transaction.payment_method.content_object
        charge_status, detail = (None, None)
        if payment_gateway == PaymentGateway.PAYONEER:
            charge_status, detail = PayoneerService.check_charge_status(payment_gateway_transaction_id)
        elif payment_gateway == PaymentGateway.PAYPAL_PRO:
            if pending_transaction.is_responded_by_payment_gateway:
                charge_status, detail = PaypalSaleService.get_payment_detail(payment_gateway_transaction_id)
            else:
                # todo handle charge after 3 hours (idempotency key were expired)
                charge_status, detail = paypal_auto_charge(invoice, payment_gateway_method, idempotency_key)
        elif payment_gateway == PaymentGateway.PAYPAL_VAULT:
            if pending_transaction.is_responded_by_payment_gateway:
                charge_status, detail = PaypalOrderService.get_order_detail(payment_gateway_transaction_id)
            else:
                # todo handle charge after 3 hours (idempotency key were expired)
                charge_status, detail = paypal_vault_auto_charge(invoice, payment_gateway_method, idempotency_key)
        else:
            logger.info(f"CHECK TRANSACTION PENDING NOT SUPPORTED YET: Gateway={pending_transaction.payment_gateway}")

        return charge_status, detail

    @classmethod
    def handle_pending_charge_after_check(cls, invoice, pending_transaction, charge_status, transaction_info):
        if transaction_info:
            transaction_form = TransactionUpdateForm(instance=pending_transaction,
                                                     data={"detail": transaction_info, "status": charge_status})
            transaction_form.validate()
            transaction_form.save()

        if charge_status == TransactionStatus.SUCCESS:
            process_success_charge(invoice)
        elif charge_status in [TransactionStatus.TRANSACTION_FAILED, TransactionStatus.CHARGE_FAILED]:
            process_failed_charge(invoice)
        else:
            process_pending_charge(invoice)
            logger.info(f"TRANSACTION STILL PENDING: ID={pending_transaction.id} Invoice={invoice.id}")
