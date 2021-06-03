class RequestType:
    FULFILL_PUSH_ORDER = "0"
    FULFILL_PUSH_ARTWORK = "1"
    FULFILL_MARK_AS_PAID = "2"
    FULFILL_UPDATE_ARTWORK = "12"
    FULFILL_UPDATE_SHIPPING_ADDRESS = "6"
    ADAPTER_FULFILL_ORDER = "3"
    ADAPTER_UPDATE_TRACKING = "4"
    ADAPTER_COMPLETE_FULFILL = "5"
    ADAPTER_ADD_NEW_PRODUCT = "7"
    ADAPTER_UPDATE_PRODUCT = "8"
    ADAPTER_UNINSTALL_APP = "9"
    ADAPTER_INIT_APP = "10"
    ADAPTER_LIST_ORDER = "11"
    ADAPTER_GET_SHIPPING_RATE = "13"
    EASY_POST_GET_TRACKING_STATUS = "14"
    ADAPTER_LIST_ORDER_BY_IDS = "15"
    ADAPTER_UPDATE_ORDER = "16"
    ADAPTER_DELETE_PRODUCT = "17"
    ADAPTER_CANCEL_FULFILL = "18"
    ADAPTER_GET_PRODUCT = '19'
    MOCKUP_GENERATE_ARTWORK_FUSION = '20'
    ADAPTER_POST_INIT_APP = '21'
    FULFILL_PRODUCTION_STATISTICS = "22"
    FULFILL_SHIPPING_STATISTICS = "23"
    ADAPTER_CHECK_SHOP_LOCATION = "24"
    PAYMENT_PAYPAL_REQUEST = "25"
    PAYMENT_PAYONEER_CHARGE = "26"
    ADAPTER_CREATE_CUSTOMIZE_PAGE = "27"


class VerboseRequestType:
    FULFILL_PUSH_ORDER = "fulfill_push_order"
    FULFILL_PUSH_ARTWORK = "fulfill_push_artwork"
    FULFILL_MARK_AS_PAID = "fulfill_mark_as_paid"
    FULFILL_UPDATE_SHIPPING_ADDRESS = "fulfill_update_shipping_address"
    FULFILL_UPDATE_ARTWORK = "fulfill_update_artwork"
    ADAPTER_FULFILL_ORDER = "adapter_fulfill_order"
    ADAPTER_UPDATE_TRACKING = "adapter_update_tracking"
    ADAPTER_COMPLETE_FULFILL = "adapter_complete_fulfill"
    ADAPTER_ADD_NEW_PRODUCT = "adapter_add_new_product"
    ADAPTER_UPDATE_PRODUCT = "adapter_update_product"
    ADAPTER_UNINSTALL_APP = "adapter_uninstall_app"
    ADAPTER_INIT_APP = "adapter_init_app"
    ADAPTER_LIST_ORDER = "adapter_list_order"
    ADAPTER_GET_SHIPPING_RATE = "adapter_get_shipping_rate"
    EASY_POST_GET_TRACKING_STATUS = "easy_post_get_tracking_status"
    ADAPTER_LIST_ORDER_BY_IDS = "adapter_list_order_by_ids"
    ADAPTER_UPDATE_ORDER = "adapter_update_order"
    ADAPTER_DELETE_PRODUCT = "adapter_delete_product"
    ADAPTER_GET_PRODUCT = "adapter_get_product"
    MOCKUP_GENERATE_ARTWORK_FUSION = "mockup_generate_artwork_fusion"
    ADAPTER_POST_INIT_APP = "adapter_post_init_app"
    FULFILL_PRODUCTION_STATISTICS = "fulfill_production_statistic"
    FULFILL_SHIPPING_STATISTICS = "fulfill_shipping_statistic"
    ADAPTER_CHECK_SHOP_LOCATION = "adapter_check_shop_location"
    PAYMENT_PAYPAL_REQUEST = "payment_paypal_request"
    PAYMENT_PAYONEER_CHARGE = "payment_payoneer_charge"
    ADAPTER_CREATE_CUSTOMIZE_PAGE = "adapter_create_customize_page"


REQUEST_TYPES = [
    (RequestType.FULFILL_PUSH_ORDER, VerboseRequestType.FULFILL_PUSH_ORDER),
    (RequestType.FULFILL_PUSH_ARTWORK, VerboseRequestType.FULFILL_PUSH_ARTWORK),
    (RequestType.FULFILL_MARK_AS_PAID, VerboseRequestType.FULFILL_MARK_AS_PAID),
    (RequestType.FULFILL_UPDATE_ARTWORK, VerboseRequestType.FULFILL_UPDATE_ARTWORK),
    (RequestType.FULFILL_UPDATE_SHIPPING_ADDRESS, VerboseRequestType.FULFILL_UPDATE_SHIPPING_ADDRESS),
    (RequestType.ADAPTER_FULFILL_ORDER, VerboseRequestType.ADAPTER_FULFILL_ORDER),
    (RequestType.ADAPTER_UPDATE_TRACKING, VerboseRequestType.ADAPTER_UPDATE_TRACKING),
    (RequestType.ADAPTER_COMPLETE_FULFILL, VerboseRequestType.ADAPTER_COMPLETE_FULFILL),
    (RequestType.ADAPTER_ADD_NEW_PRODUCT, VerboseRequestType.ADAPTER_ADD_NEW_PRODUCT),
    (RequestType.ADAPTER_UPDATE_PRODUCT, VerboseRequestType.ADAPTER_UPDATE_PRODUCT),
    (RequestType.ADAPTER_UNINSTALL_APP, VerboseRequestType.ADAPTER_UNINSTALL_APP),
    (RequestType.ADAPTER_INIT_APP, VerboseRequestType.ADAPTER_INIT_APP),
    (RequestType.ADAPTER_LIST_ORDER, VerboseRequestType.ADAPTER_LIST_ORDER),
    (RequestType.ADAPTER_GET_SHIPPING_RATE, VerboseRequestType.ADAPTER_GET_SHIPPING_RATE),
    (RequestType.EASY_POST_GET_TRACKING_STATUS, VerboseRequestType.EASY_POST_GET_TRACKING_STATUS),
    (RequestType.ADAPTER_LIST_ORDER_BY_IDS, VerboseRequestType.ADAPTER_LIST_ORDER_BY_IDS),
    (RequestType.ADAPTER_UPDATE_ORDER, VerboseRequestType.ADAPTER_UPDATE_ORDER),
    (RequestType.ADAPTER_DELETE_PRODUCT, VerboseRequestType.ADAPTER_DELETE_PRODUCT),
    (RequestType.ADAPTER_GET_PRODUCT, VerboseRequestType.ADAPTER_GET_PRODUCT),
    (RequestType.MOCKUP_GENERATE_ARTWORK_FUSION, VerboseRequestType.MOCKUP_GENERATE_ARTWORK_FUSION),
    (RequestType.ADAPTER_POST_INIT_APP, VerboseRequestType.ADAPTER_POST_INIT_APP),
    (RequestType.FULFILL_PRODUCTION_STATISTICS, VerboseRequestType.FULFILL_PRODUCTION_STATISTICS),
    (RequestType.FULFILL_SHIPPING_STATISTICS, VerboseRequestType.FULFILL_SHIPPING_STATISTICS),
    (RequestType.ADAPTER_CHECK_SHOP_LOCATION, VerboseRequestType.ADAPTER_CHECK_SHOP_LOCATION),
    (RequestType.PAYMENT_PAYPAL_REQUEST, VerboseRequestType.PAYMENT_PAYPAL_REQUEST),
    (RequestType.PAYMENT_PAYONEER_CHARGE, VerboseRequestType.PAYMENT_PAYONEER_CHARGE),
    (RequestType.ADAPTER_CREATE_CUSTOMIZE_PAGE, VerboseRequestType.ADAPTER_CREATE_CUSTOMIZE_PAGE)
]

REQUEST_TYPES_LIST = [[verbose, code] for code, verbose in REQUEST_TYPES]
