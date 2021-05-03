class InvoicePackStatus:
    CANCELED = '-1'
    UNPAID = '0'
    PAID = '1'
    FAILED = '2'
    REFUNDED = '3'


class VerboseInvoicePackStatus:
    CANCELED = 'canceled'
    UNPAID = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    REFUNDED = 'refunded'


INVOICE_PACK_STATUS_CHOICES = [
    (InvoicePackStatus.CANCELED, VerboseInvoicePackStatus.CANCELED),
    (InvoicePackStatus.UNPAID, VerboseInvoicePackStatus.UNPAID),
    (InvoicePackStatus.PAID, VerboseInvoicePackStatus.PAID),
    (InvoicePackStatus.FAILED, VerboseInvoicePackStatus.FAILED),
    (InvoicePackStatus.REFUNDED, VerboseInvoicePackStatus.REFUNDED),
]

INVOICE_PACK_STATUSES_CANCELLABLE = [InvoicePackStatus.UNPAID, InvoicePackStatus.FAILED]
