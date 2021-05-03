class InvoiceProcessStatus:
    SUCCESS = '1'
    PROCESSING = '0'
    FAILED = '-1'


class VerboseInvoiceProcessStatus:
    SUCCESS = 'success'
    FAILED = 'failed'


INVOICE_PROCESS_STATUS_CHOICES = [
    (InvoiceProcessStatus.SUCCESS, VerboseInvoiceProcessStatus.SUCCESS),
    (InvoiceProcessStatus.FAILED, VerboseInvoiceProcessStatus.FAILED)
]
