class TransactionStatus:
    CHARGE_FAILED = '0'
    SUCCESS = '1'
    TRANSACTION_FAILED = '2'
    TRANSACTION_PENDING = '3'
    CANCELED = '4'


class VerboseTransactionStatus:
    CHARGE_FAILED = 'failed'
    SUCCESS = 'success'
    TRANSACTION_FAILED = 'transaction_failed'
    TRANSACTION_PENDING = 'transaction_pending'
    CANCELED = 'canceled'


TRANSACTION_STATUS_CHOICES = [
    (TransactionStatus.CHARGE_FAILED, VerboseTransactionStatus.CHARGE_FAILED),
    (TransactionStatus.SUCCESS, VerboseTransactionStatus.SUCCESS),
    (TransactionStatus.TRANSACTION_FAILED, VerboseTransactionStatus.TRANSACTION_FAILED),
    (TransactionStatus.TRANSACTION_PENDING, VerboseTransactionStatus.TRANSACTION_PENDING),
    (TransactionStatus.CANCELED, VerboseTransactionStatus.CANCELED),
]

TRANSACTION_STATUS_DICT = {status: verbose for status, verbose in TRANSACTION_STATUS_CHOICES}

FAILED_TRANSACTION_STATUSES = [TransactionStatus.CHARGE_FAILED, TransactionStatus.TRANSACTION_FAILED]
SUCCESS_TRANSACTION_STATUSES = [TransactionStatus.CHARGE_FAILED, TransactionStatus.TRANSACTION_FAILED]
