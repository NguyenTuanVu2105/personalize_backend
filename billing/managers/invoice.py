from datetime import timedelta

from django.db.models import Manager, QuerySet, Prefetch, Sum, F, Case, When, DecimalField

from HUB import settings
from HUB.helpers.sql.functions import Round
from billing.constants.invoice_pack_statuses import InvoicePackStatus
from billing.constants.invoice_statuses import InvoiceStatus
from helper.datetime_helpers import get_current_datetime


class BaseInvoiceManager(Manager):
    def get_queryset(self):
        from billing.models import Transaction

        return super().get_queryset().prefetch_related(
            Prefetch("transactions", queryset=Transaction.objects.filter_charge_type().success(),
                     to_attr="success_transactions")).annotate(
            total_cost=Round(Sum(
                Case(When(packs__status=InvoicePackStatus.CANCELED, then=0),
                     default=F("packs__production_cost") + F("packs__shipping_cost") - F("packs__discount") + F("packs__tax")),
                output_field=DecimalField(),
            )))


class InvoiceQueryset(QuerySet):
    def unpaid(self):
        return self.filter(status=InvoiceStatus.UNPAID)

    def failed(self):
        return self.filter(status=InvoiceStatus.FAILED)

    def unpaid_or_failed(self):
        return self.filter(status__in=(InvoiceStatus.UNPAID, InvoiceStatus.FAILED))

    def transaction_pending(self):
        return self.filter(status=InvoiceStatus.TRANSACTION_PENDING)

    def last_updated_earlier_x_min_ago(self, x):
        return self.filter(update_time__lte=get_current_datetime() - timedelta(minutes=x)).order_by("update_time")

    def filter_by_chargeable_customers(self):
        current_time = get_current_datetime()
        return self.filter(customer__settings__next_charge_time__lte=current_time)

    def filter_customer(self, customer_id):
        return self.filter(customer_id=customer_id)

    def create_with_customer(self, customer, **kwargs):
        status = InvoiceStatus.UNPAID
        if customer.settings.should_halt_to_charge_invoices:
            status = InvoiceStatus.FAILED
        return self.create(**kwargs, customer=customer, status=status)

    def get_by_payment_gateway_invoice_id(self, payment_gateway_invoice_id):
        id_prefix = settings.IDEMPOTENCY_KEY_PREFIX
        if not payment_gateway_invoice_id or not payment_gateway_invoice_id.startswith(id_prefix):
            return None
        invoice_id_start_index = len(id_prefix)
        invoice_id = payment_gateway_invoice_id[invoice_id_start_index:]
        return self.filter(id=invoice_id).first()


InvoiceManager = BaseInvoiceManager.from_queryset(InvoiceQueryset)
