class InvoiceStatus:
    CANCELED = '-1'
    UNPAID = '0'
    PAID = '1'
    FAILED = '2'
    PENDING = '3'
    PROCESSING = '4'
    TRANSACTION_PENDING = '5'


class VerboseInvoiceStatus:
    CANCELED = 'canceled'
    UNPAID = 'unpaid'
    PAID = 'paid'
    FAILED = 'failed'
    PENDING = 'pending'
    PROCESSING = 'processing'
    TRANSACTION_PENDING = 'transaction_pending'


INVOICE_STATUS_CHOICES = [
    (InvoiceStatus.CANCELED, VerboseInvoiceStatus.CANCELED),
    (InvoiceStatus.UNPAID, VerboseInvoiceStatus.UNPAID),
    (InvoiceStatus.PAID, VerboseInvoiceStatus.PAID),
    (InvoiceStatus.FAILED, VerboseInvoiceStatus.FAILED),
    (InvoiceStatus.PROCESSING, VerboseInvoiceStatus.PROCESSING),
    (InvoiceStatus.PENDING, VerboseInvoiceStatus.PENDING),
    (InvoiceStatus.TRANSACTION_PENDING, VerboseInvoiceStatus.TRANSACTION_PENDING)
]
