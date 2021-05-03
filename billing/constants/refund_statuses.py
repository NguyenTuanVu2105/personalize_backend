class RefundStatus:
    PENDING = '0'
    SETTLED = '1'
    FAILED = '2'
    REJECTED = '3'
    IN_REVIEW = '4'


class VerboseRefundStatus:
    PENDING = 'pending'
    SETTLED = 'settled'
    FAILED = 'failed'
    REJECTED = 'rejected'
    IN_REVIEW = 'in_review'


REFUND_STATUSES = [
    (RefundStatus.PENDING, VerboseRefundStatus.PENDING),
    (RefundStatus.SETTLED, VerboseRefundStatus.SETTLED),
    (RefundStatus.FAILED, VerboseRefundStatus.FAILED),
    (RefundStatus.REJECTED, VerboseRefundStatus.REJECTED),
    (RefundStatus.IN_REVIEW, VerboseRefundStatus.IN_REVIEW)
]
