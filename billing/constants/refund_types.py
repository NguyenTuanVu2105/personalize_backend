class RefundType:
    CANCEL_SHIPPING = '1'
    REJECT_ORDER_ITEMS = '2'
    PAY_BACK_MANUALLY = '3'


class VerboseRefundType:
    CANCEL_SHIPPING = 'cancel_shipping'
    REJECT_ORDER_ITEMS = 'reject_order_items'
    PAY_BACK_MANUALLY = 'pay_back_manually'


REFUND_TYPES = [
    (RefundType.CANCEL_SHIPPING, VerboseRefundType.CANCEL_SHIPPING),
    (RefundType.REJECT_ORDER_ITEMS, VerboseRefundType.REJECT_ORDER_ITEMS),
    (RefundType.PAY_BACK_MANUALLY, VerboseRefundType.PAY_BACK_MANUALLY)
]

REFUND_TYPE_DICT = {status: verbose for status, verbose in REFUND_TYPES}
