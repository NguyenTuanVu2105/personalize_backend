from django.db.models import Manager, QuerySet, Sum, F

from billing.constants.invoice_pack_statuses import INVOICE_PACK_STATUSES_CANCELLABLE
from billing.constants.invoice_pack_statuses import InvoicePackStatus


class BaseInvoicePackManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("invoice")


class InvoicePackQueryset(QuerySet):
    def unpaid(self):
        return self.filter(status=InvoicePackStatus.UNPAID)

    def failed(self):
        return self.filter(status=InvoicePackStatus.FAILED)

    def unpaid_or_failed(self):
        return self.filter(status__in=(InvoicePackStatus.UNPAID, InvoicePackStatus.FAILED))

    def cancellable(self):
        return self.filter(status__in=INVOICE_PACK_STATUSES_CANCELLABLE)

    def not_canceled(self):
        return self.exclude(status=InvoicePackStatus.CANCELED)

    def bulk_set_paid(self):
        return self.unpaid_or_failed().update(status=InvoicePackStatus.PAID)

    def bulk_set_canceled(self):
        return self.cancellable().update(status=InvoicePackStatus.CANCELED)

    def bulk_set_failed(self):
        return self.unpaid().update(status=InvoicePackStatus.FAILED)

    def bulk_set_unpaid(self):
        return self.failed().update(status=InvoicePackStatus.UNPAID)

    def merge_to_new_invoice(self, invoice_obj):
        return self.update(invoice=invoice_obj, status=invoice_obj.status)

    def aggregate_total_cost(self):
        return self.not_canceled().aggregate(total_cost=Sum(F("production_cost") + F("shipping_cost") + F("tax"))).get(
            "total_cost") or 0


InvoicePackManager = BaseInvoicePackManager.from_queryset(InvoicePackQueryset)
