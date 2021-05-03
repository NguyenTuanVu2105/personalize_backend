class InvalidReasonType:
    ORDER_EXISTED = '4'
    ITEM_NOT_IN_PRINTHOLO = '5'
    SHOP_INVALID = '6'
    UNPAID_ORDER = '7'
    PARTIAL_ITEM_IN_PRINTHOLO = '9'
    OTHER = '8'


class VerboseInvalidReasonType:
    ORDER_EXISTED = 'order_existed'
    ITEM_NOT_IN_PRINTHOLO = 'item_not_in_printholo'
    SHOP_INVALID = 'shop_invalid'
    UNPAID_ORDER = 'unpaid_order'
    PARTIAL_ITEM_IN_PRINTHOLO = 'partial_item_in_printholo'
    OTHER = 'other'


INVALID_REASON_TYPE_CHOICES = (
    (InvalidReasonType.ORDER_EXISTED, VerboseInvalidReasonType.ORDER_EXISTED),
    (InvalidReasonType.ITEM_NOT_IN_PRINTHOLO, VerboseInvalidReasonType.ITEM_NOT_IN_PRINTHOLO),
    (InvalidReasonType.SHOP_INVALID, VerboseInvalidReasonType.SHOP_INVALID),
    (InvalidReasonType.UNPAID_ORDER, VerboseInvalidReasonType.UNPAID_ORDER),
    (InvalidReasonType.OTHER, VerboseInvalidReasonType.OTHER),
    (InvalidReasonType.PARTIAL_ITEM_IN_PRINTHOLO, VerboseInvalidReasonType.PARTIAL_ITEM_IN_PRINTHOLO)
)

DescriptionInvalidReason = {
    InvalidReasonType.ORDER_EXISTED: "Order is existed in printholo.",
    InvalidReasonType.ITEM_NOT_IN_PRINTHOLO: "No product item in printholo",
    InvalidReasonType.SHOP_INVALID: "Shop is invalid",
    InvalidReasonType.UNPAID_ORDER: "Order is unpaid so it cannot sync in printholo.",
    InvalidReasonType.OTHER: "Order failed because other reason.",
    InvalidReasonType.PARTIAL_ITEM_IN_PRINTHOLO: "Some product item maybe not in printholo or deleted."
}