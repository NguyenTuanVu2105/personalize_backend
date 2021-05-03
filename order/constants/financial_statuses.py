class OrderFinancialStatus:
    PENDING = "1"
    PARTIALLY_PAID = "2"
    PAID = "3"
    CANCELED = "4"
    FAILED = "5"


class VerboseOrderFinancialStatus:
    PENDING = "pending"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    CANCELED = "canceled"
    FAILED = "failed"


ORDER_FINANCIAL_STATUS_CHOICES = [
    (OrderFinancialStatus.PENDING, VerboseOrderFinancialStatus.PENDING),
    (OrderFinancialStatus.PAID, VerboseOrderFinancialStatus.PAID),
    (OrderFinancialStatus.PARTIALLY_PAID, VerboseOrderFinancialStatus.PARTIALLY_PAID),
    (OrderFinancialStatus.CANCELED, VerboseOrderFinancialStatus.CANCELED),
    (OrderFinancialStatus.FAILED, VerboseOrderFinancialStatus.FAILED),
]

ORDER_FINANCIAL_STATUSES_CANCELLABLE = [OrderFinancialStatus.PENDING, OrderFinancialStatus.FAILED]
ORDER_PACK_FINANCIAL_STATUSES_CANCELLABLE = [OrderFinancialStatus.PENDING, OrderFinancialStatus.FAILED]
