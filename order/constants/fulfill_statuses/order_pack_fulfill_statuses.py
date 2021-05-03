class OrderPackFulfillStatus:
    UNFULFILLED = "0"
    PENDING = "1"
    IN_PRODUCTION = "2"
    FULFILLED = "3"
    CANCELED = "4"
    CANCELED_SHIPPING = "5"
    REJECTED = "6"
    REQUESTED_FULFILLMENT = "7"
    HOLDING = "8"  # keep order in hold status, do nothing


class VerboseOrderPackFulfillStatus:
    UNFULFILLED = "unfulfilled"
    PENDING = "pending"
    IN_PRODUCTION = "in_production"
    FULFILLED = "fulfilled"
    CANCELED = "canceled"
    CANCELED_SHIPPING = "canceled_shipping"
    REJECTED = "rejected"
    REQUESTED_FULFILLMENT = "requested_fulfillment"
    HOLDING = "holding"


ORDER_PACK_STATUS_CHOICES = (
    (OrderPackFulfillStatus.UNFULFILLED, VerboseOrderPackFulfillStatus.UNFULFILLED),
    (OrderPackFulfillStatus.PENDING, VerboseOrderPackFulfillStatus.PENDING),
    (OrderPackFulfillStatus.IN_PRODUCTION, VerboseOrderPackFulfillStatus.IN_PRODUCTION),
    (OrderPackFulfillStatus.FULFILLED, VerboseOrderPackFulfillStatus.FULFILLED),
    (OrderPackFulfillStatus.CANCELED, VerboseOrderPackFulfillStatus.CANCELED),
    (OrderPackFulfillStatus.CANCELED_SHIPPING, VerboseOrderPackFulfillStatus.CANCELED_SHIPPING),
    (OrderPackFulfillStatus.REJECTED, VerboseOrderPackFulfillStatus.REJECTED),
    (OrderPackFulfillStatus.REQUESTED_FULFILLMENT, VerboseOrderPackFulfillStatus.REQUESTED_FULFILLMENT),
    (OrderPackFulfillStatus.HOLDING, VerboseOrderPackFulfillStatus.HOLDING)
)

ORDER_PACK_STATUS_VERBOSE_DICT = {status: verbose for status, verbose in ORDER_PACK_STATUS_CHOICES}

ORDER_PACK_STATUSES_HAS_TRACKING = [OrderPackFulfillStatus.FULFILLED]
ORDER_PACK_FULFILL_STATUSES_CANCELLABLE = [OrderPackFulfillStatus.UNFULFILLED, OrderPackFulfillStatus.PENDING,
                                           OrderPackFulfillStatus.HOLDING]
