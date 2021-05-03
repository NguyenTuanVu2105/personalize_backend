class TransactionType:
    REFUND = '0'
    CHARGE = '1'


class VerboseTransactionType:
    REFUND = 'refund'
    CHARGE = 'charge'


TRANSACTION_TYPE_CHOICES = [
    (TransactionType.REFUND, VerboseTransactionType.REFUND),
    (TransactionType.CHARGE, VerboseTransactionType.CHARGE),
]
