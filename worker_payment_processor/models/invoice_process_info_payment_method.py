from django.db import models

from billing.sub_apps.combine_payment.models import GeneralPaymentMethod
from worker_payment_processor.models import InvoiceProcessInfo


class InvoiceProcessInfoPaymentMethod(models.Model):
    invoice_process_info = models.ForeignKey(to=InvoiceProcessInfo, related_name="payment_method_mappings", on_delete=models.CASCADE)
    payment_method = models.ForeignKey(to=GeneralPaymentMethod, related_name="invoice_process_info_mappings", on_delete=models.CASCADE)
    ordinal_number = models.SmallIntegerField(default=0)

    class Meta:
        db_table = "billing_invoice_process_info_payment_method"
        ordering = ['ordinal_number', 'id']
