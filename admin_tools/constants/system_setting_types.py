class SystemSettingTypes:
    AUTO_SEND_SHIPPING_ORDER_NOTIFICATION = '1'
    AUTO_SEND_DELIVERED_ORDER_NOTIFICATION = '2'
    FFM_SERVICE_SETTING = '3'
    AUTO_SEND_UNPROFITABLE_ORDER_NOTIFICATION = '4'
    AUTO_SEND_ORDER_REVIEW = '5'
    AUTO_SEND_ADD_PAYMENT_NOTIFICATION = '6'
    SCHEDULE_UPDATE_TRACKER = '7'

class VerboseSystemSettingTypes:
    AUTO_SEND_SHIPPING_ORDER_NOTIFICATION = 'auto_send_shipping_order_notification'
    AUTO_SEND_DELIVERED_ORDER_NOTIFICATION = 'auto_send_delivered_order_notification'
    FFM_SERVICE_SETTING = 'ffm_service_setting'
    AUTO_SEND_UNPROFITABLE_ORDER_NOTIFICATION = 'auto_send_unprofitable_order_notification'
    AUTO_SEND_ORDER_REVIEW = 'auto_send_order_review'
    AUTO_SEND_ADD_PAYMENT_NOTIFICATION = 'auto_send_add_payment_notification'
    SCHEDULE_UPDATE_TRACKER = 'schedule_update_tracker'

SYSTEM_SETTING_TYPE_CHOICES = (
    (SystemSettingTypes.AUTO_SEND_SHIPPING_ORDER_NOTIFICATION,
     VerboseSystemSettingTypes.AUTO_SEND_SHIPPING_ORDER_NOTIFICATION),
    (SystemSettingTypes.AUTO_SEND_DELIVERED_ORDER_NOTIFICATION,
     VerboseSystemSettingTypes.AUTO_SEND_DELIVERED_ORDER_NOTIFICATION),
    (SystemSettingTypes.FFM_SERVICE_SETTING,
     VerboseSystemSettingTypes.FFM_SERVICE_SETTING),
    (SystemSettingTypes.AUTO_SEND_UNPROFITABLE_ORDER_NOTIFICATION,
     VerboseSystemSettingTypes.AUTO_SEND_UNPROFITABLE_ORDER_NOTIFICATION),
    (SystemSettingTypes.AUTO_SEND_ORDER_REVIEW, VerboseSystemSettingTypes.AUTO_SEND_ORDER_REVIEW),
    (SystemSettingTypes.AUTO_SEND_ADD_PAYMENT_NOTIFICATION, VerboseSystemSettingTypes.AUTO_SEND_ADD_PAYMENT_NOTIFICATION),
    (SystemSettingTypes.SCHEDULE_UPDATE_TRACKER, VerboseSystemSettingTypes.SCHEDULE_UPDATE_TRACKER)
)
