import logging
import platform

from django.db import transaction

from billing.constants.invoice_statuses import InvoiceStatus
from billing.constants.transaction_statuses import TransactionStatus
from billing.functions.get_idempotency_key import get_idempotency_key
from billing.models import Invoice
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod
from worker_payment_processor.exceptions.duplicate_charge_exception import DuplicateChargeException
from worker_payment_processor.models import InvoiceProcessInfoPaymentMethod
from worker_payment_processor.models.invoice_process_info import InvoiceProcessInfo

logger = logging.getLogger(__name__)


@transaction.atomic
def check_invoice(invoice_id, charge_count):
    charge_count = charge_count + 1
    invoice_process_info_id = get_invoice_processing_info_key(invoice_id, charge_count)
    logger.info(f'{invoice_process_info_id}')
    if InvoiceProcessInfo.objects.filter(id=invoice_process_info_id).exists():
        raise DuplicateChargeException()
    invoice = Invoice.objects.get(pk=invoice_id)
    invoice_owner = invoice.customer
    payment_methods = GeneralPaymentMethod.objects.active().by_user(invoice_owner.pk)

    invoice.status = InvoiceStatus.PROCESSING
    invoice.charge_count = charge_count
    invoice.save()

    invoice_process_info = InvoiceProcessInfo.objects.create(id=invoice_process_info_id,
                                                             invoice=invoice,
                                                             worker_host=platform.node())
    InvoiceProcessInfoPaymentMethod.objects.bulk_create(
        [InvoiceProcessInfoPaymentMethod(invoice_process_info=invoice_process_info,
                                         payment_method=method,
                                         ordinal_number=method.ordinal_number) for method in payment_methods]
    )
    return invoice_process_info


def get_invoice_idempotency_key(invoice):
    exist_idempotency_keys = invoice.transactions.filter(status=TransactionStatus.TRANSACTION_FAILED).values_list("idempotency_key", flat=True)
    logger.info(exist_idempotency_keys)
    new_idempotency_key = get_idempotency_key(invoice.id, exist_idempotency_keys)
    logger.info(f'New idempotency_key = {new_idempotency_key} ')
    return new_idempotency_key


def get_invoice_processing_info_key(invoice_id, charge_count):
    return f'{invoice_id}t{charge_count}'
