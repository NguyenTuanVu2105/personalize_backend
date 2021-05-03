class OrderItemFulfillStatus:
    ACCEPTED = "1"
    REJECTED = "2"
    HOLDING = "3"


class VerboseOrderItemFulfillStatus:
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    HOLDING = "holding"


ORDER_ITEM_FULFILL_STATUS_CHOICES = (
    (OrderItemFulfillStatus.ACCEPTED, VerboseOrderItemFulfillStatus.ACCEPTED),
    (OrderItemFulfillStatus.REJECTED, VerboseOrderItemFulfillStatus.REJECTED),
    (OrderItemFulfillStatus.HOLDING, VerboseOrderItemFulfillStatus.HOLDING),
)

ORDER_ITEM_FULFILL_STATUS_VERBOSE_DICT = {verbose: status for status, verbose in ORDER_ITEM_FULFILL_STATUS_CHOICES}
ORDER_ITEM_FULFILL_STATUS_DICT = {status: verbose for status, verbose in ORDER_ITEM_FULFILL_STATUS_CHOICES}
