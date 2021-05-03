import json
import logging

from celery.execute import send_task
from django.db import transaction

from HUB.constants.celery_task import CeleryTask
from billing.constants.invoice_statuses import InvoiceStatus
from billing.models import Invoice
from billing.sub_apps.combine_payment.constants.charge_constants import NUMBER_OF_INVOICE_PER_SCHEDULE_RUN, DELAY_X_MIN_INVOICE_CHARGE_AFTER_UPDATED

logger = logging.getLogger(__name__)


def auto_charging():
    chargeable_invoices = Invoice.objects.unpaid(). \
                              filter_by_chargeable_customers(). \
                              last_updated_earlier_x_min_ago(DELAY_X_MIN_INVOICE_CHARGE_AFTER_UPDATED)
    selected_chargeable_invoices = chargeable_invoices[:NUMBER_OF_INVOICE_PER_SCHEDULE_RUN]
    for invoice in selected_chargeable_invoices:
        request_charge_invoice(invoice)
    return len(selected_chargeable_invoices)


@transaction.atomic
def request_charge_invoice(invoice):
    send_task(CeleryTask.TASK_CHARGE_INVOICE, [json.dumps({"invoice_id": invoice.id, "charge_count": invoice.charge_count})])
    invoice.status = InvoiceStatus.PENDING
    invoice.save()
