from django.db import models

from billing.models import Invoice
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod


class InvoiceProcessInfo(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE, related_name="processor_info")
    payment_methods = models.ManyToManyField(to=GeneralPaymentMethod, related_name="invoice_processor_info_set",  through="worker_payment_processor.InvoiceProcessInfoPaymentMethod")
    worker_host = models.CharField(max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'billing_invoice_processor_info'
        ordering = ['id']
