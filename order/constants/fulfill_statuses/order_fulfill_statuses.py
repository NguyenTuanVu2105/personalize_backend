class OrderFulfillStatus:
    FULFILLED = "1"
    PARTIALLY_FULFILLED = "2"
    IN_PRODUCTION = "3"
    PARTIALLY_IN_PRODUCTION = "4"
    UNFULFILLED = "5"
    PENDING = "6"
    CANCELED = "7"
    CANCELED_SHIPPING = "8"
    REJECTED = "9"
    REQUESTED_FULFILLMENT = "10"
    HOLDING = "11"  # keep order in hold status, do nothing


class VerboseOrderFulfillStatus:
    FULFILLED = "fulfilled"
    PARTIALLY_FULFILLED = "partially_fulfilled"
    IN_PRODUCTION = "in_production"
    PARTIALLY_IN_PRODUCTION = "partially_in_production"
    UNFULFILLED = "unfulfilled"
    PENDING = "pending"
    CANCELED = "canceled"
    CANCELED_SHIPPING = "canceled_shipping"
    REJECTED = "rejected"
    REQUESTED_FULFILLMENT = "requested_fulfillment"
    HOLDING = "holding"


ORDER_FULFILL_STATUS_CHOICES = (
    (OrderFulfillStatus.UNFULFILLED, VerboseOrderFulfillStatus.UNFULFILLED),
    (OrderFulfillStatus.PENDING, VerboseOrderFulfillStatus.PENDING),
    (OrderFulfillStatus.IN_PRODUCTION, VerboseOrderFulfillStatus.IN_PRODUCTION),
    (OrderFulfillStatus.PARTIALLY_IN_PRODUCTION, VerboseOrderFulfillStatus.PARTIALLY_IN_PRODUCTION),
    (OrderFulfillStatus.FULFILLED, VerboseOrderFulfillStatus.FULFILLED),
    (OrderFulfillStatus.PARTIALLY_FULFILLED, VerboseOrderFulfillStatus.PARTIALLY_FULFILLED),
    (OrderFulfillStatus.CANCELED, VerboseOrderFulfillStatus.CANCELED),
    (OrderFulfillStatus.CANCELED_SHIPPING, VerboseOrderFulfillStatus.CANCELED_SHIPPING),
    (OrderFulfillStatus.REJECTED, VerboseOrderFulfillStatus.REJECTED),
    (OrderFulfillStatus.REQUESTED_FULFILLMENT, VerboseOrderFulfillStatus.REQUESTED_FULFILLMENT),
    (OrderFulfillStatus.HOLDING, VerboseOrderFulfillStatus.HOLDING),
)

ORDER_FULFILL_STATUSES_CANCELLABLE = [OrderFulfillStatus.UNFULFILLED, OrderFulfillStatus.HOLDING]
ORDER_STATUSES_ALLOW_UPDATE_SHIPPING = [OrderFulfillStatus.UNFULFILLED, OrderFulfillStatus.PENDING,
                                        OrderFulfillStatus.REQUESTED_FULFILLMENT, OrderFulfillStatus.HOLDING]
ORDER_STATUSES_ALLOW_UPDATE_ITEM = [OrderFulfillStatus.UNFULFILLED, OrderFulfillStatus.HOLDING]
