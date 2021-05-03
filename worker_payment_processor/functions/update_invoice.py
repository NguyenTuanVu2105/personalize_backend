import logging

from django.db import transaction

from HUB.exceptions.FormValidationError import FormValidationError
from billing.constants.transaction_statuses import TransactionStatus
from billing.forms import TransactionCreationForm
from billing.sub_apps.combine_payment.functions.charge_result_handling import process_failed_charge, \
    process_pending_charge, process_success_charge, process_canceled_charge

logger = logging.getLogger(__name__)


@transaction.atomic
def update_invoice(invoice_process_info, charge_status, transactions):
    invoice_obj = invoice_process_info.invoice
    if charge_status in [TransactionStatus.CHARGE_FAILED, TransactionStatus.TRANSACTION_FAILED]:
        process_failed_charge(invoice_obj)
    elif charge_status == TransactionStatus.TRANSACTION_PENDING:
        process_pending_charge(invoice_obj)
    elif charge_status == TransactionStatus.SUCCESS:
        process_success_charge(invoice_obj)
    elif charge_status == TransactionStatus.CANCELED:
        process_canceled_charge(invoice_obj)
    saved_transactions = save_all_transaction(transactions)
    return invoice_obj, saved_transactions


def save_all_transaction(transactions):
    saved_transactions = []
    for transaction_data in transactions:
        saved_transactions.append(save_new_transaction(transaction_data))
    return saved_transactions


def save_new_transaction(transaction_data):
    form = TransactionCreationForm(data=transaction_data)
    if not form.is_valid():
        logger.warning(form.errors.get_json_data())
        raise FormValidationError(errors=form.errors.get_json_data())
    transaction_obj = form.save()
    logger.info("Saved new {} transaction".format(transaction_obj.verbose_type))
    return transaction_obj
