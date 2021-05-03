class OrderHistoryType:
    CREATE_ORDER = "1"
    UPDATE_ORDER_FULFILL_STATUS = "2"
    UPDATE_ORDER_FINANCIAL_STATUS = "3"
    UPDATE_ORDER_SHIPPING_ADDRESS = "4"
    UPDATE_ORDER_SHIPPING_RATE = "7"
    UPDATE_ORDER_ITEM_VARIANT = "5"
    UPDATE_ORDER_ITEM_QUANTITY = "6"
    UPDATE_ORDER_IS_ITEM_EDITABLE_STATUS = "8"
    CREATE_SUPPORT_TICKET = "9"
    UPDATE_SUPPORT_TICKET = "10"
    REJECT_ITEM_BY_FULFILL = "11"
    REJECT_NOT_SUPPORT_SHIPPING_ITEM = "12"
    REJECT_NO_SHIPPING_ITEM = "13"
    REJECT_ORDER_BY_FULFILL = "14"
    REMOVE_ORDER_ITEM = "15"
    ADD_ORDER_ITEM = "16"


class VerboseOrderHistoryType:
    CREATE_ORDER = "create_order"
    UPDATE_ORDER_FULFILL_STATUS = "update_order_fulfill_status"
    UPDATE_ORDER_FINANCIAL_STATUS = "update_order_financial_status"
    UPDATE_ORDER_SHIPPING_ADDRESS = "update_order_shipping_address"
    UPDATE_ORDER_SHIPPING_RATE = "update_order_shipping_rate"
    UPDATE_ORDER_ITEM_VARIANT = "update_order_item_variant"
    UPDATE_ORDER_ITEM_QUANTITY = "update_order_item_quantity"
    UPDATE_ORDER_IS_ITEM_EDITABLE_STATUS = "update_order_is_item_editable_status"
    CREATE_SUPPORT_TICKET = "create_support_ticket"
    UPDATE_SUPPORT_TICKET = "update_support_ticket"
    REJECT_ITEM_BY_FULFILL = "reject_item_by_fulfill"
    REJECT_NOT_SUPPORT_SHIPPING_ITEM = "reject_not_support_shipping_item"
    REJECT_NO_SHIPPING_ITEM = "reject_no_shipping_item"
    REJECT_ORDER_BY_FULFILL = "reject_order_by_fulfill"
    REMOVE_ORDER_ITEM = "remove_order_item"
    ADD_ORDER_ITEM = "add_order_item"


ORDER_HISTORY_TYPE_CHOICES = [
    (OrderHistoryType.CREATE_ORDER, VerboseOrderHistoryType.CREATE_ORDER),
    (OrderHistoryType.UPDATE_ORDER_FULFILL_STATUS, VerboseOrderHistoryType.UPDATE_ORDER_FULFILL_STATUS),
    (OrderHistoryType.UPDATE_ORDER_FINANCIAL_STATUS, VerboseOrderHistoryType.UPDATE_ORDER_FINANCIAL_STATUS),
    (OrderHistoryType.UPDATE_ORDER_SHIPPING_ADDRESS, VerboseOrderHistoryType.UPDATE_ORDER_SHIPPING_ADDRESS),
    (OrderHistoryType.UPDATE_ORDER_SHIPPING_RATE, VerboseOrderHistoryType.UPDATE_ORDER_SHIPPING_RATE),
    (OrderHistoryType.UPDATE_ORDER_ITEM_VARIANT, VerboseOrderHistoryType.UPDATE_ORDER_ITEM_VARIANT),
    (OrderHistoryType.UPDATE_ORDER_ITEM_QUANTITY, VerboseOrderHistoryType.UPDATE_ORDER_ITEM_QUANTITY),
    (OrderHistoryType.UPDATE_ORDER_IS_ITEM_EDITABLE_STATUS, VerboseOrderHistoryType.UPDATE_ORDER_IS_ITEM_EDITABLE_STATUS),
    (OrderHistoryType.CREATE_SUPPORT_TICKET, VerboseOrderHistoryType.CREATE_SUPPORT_TICKET),
    (OrderHistoryType.UPDATE_SUPPORT_TICKET, VerboseOrderHistoryType.UPDATE_SUPPORT_TICKET),
    (OrderHistoryType.REJECT_ITEM_BY_FULFILL, VerboseOrderHistoryType.REJECT_ITEM_BY_FULFILL),
    (OrderHistoryType.REJECT_NOT_SUPPORT_SHIPPING_ITEM, VerboseOrderHistoryType.REJECT_NOT_SUPPORT_SHIPPING_ITEM),
    (OrderHistoryType.REJECT_NO_SHIPPING_ITEM, VerboseOrderHistoryType.REJECT_NO_SHIPPING_ITEM),
    (OrderHistoryType.REJECT_ORDER_BY_FULFILL, VerboseOrderHistoryType.REJECT_ORDER_BY_FULFILL),
    (OrderHistoryType.REMOVE_ORDER_ITEM, VerboseOrderHistoryType.REMOVE_ORDER_ITEM),
    (OrderHistoryType.ADD_ORDER_ITEM, VerboseOrderHistoryType.ADD_ORDER_ITEM)
]
