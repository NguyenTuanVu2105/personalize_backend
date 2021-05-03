from notification.enums.message_types import MessageType


class OrderTrackingNotificationType:
    ORDER_SHIPPING_NOTICE = '1'
    ORDER_DELIVERED_NOTICE = '2'


class OrderTrackingNotificationTypeVerbose:
    ORDER_SHIPPING_NOTICE = 'order shipping'
    ORDER_DELIVERED_NOTICE = 'order delivered'


ORDER_TRACKING_NOTIFICATION_TYPE_CHOICES = (
    (OrderTrackingNotificationType.ORDER_SHIPPING_NOTICE, OrderTrackingNotificationTypeVerbose.ORDER_SHIPPING_NOTICE),
    (OrderTrackingNotificationType.ORDER_DELIVERED_NOTICE, OrderTrackingNotificationTypeVerbose.ORDER_DELIVERED_NOTICE),
)

ORDER_NOTIFICATION_CORRESPONDING_EMAIL_TYPE_TUPLE = (
    (OrderTrackingNotificationType.ORDER_SHIPPING_NOTICE, MessageType.ORDER_SHIPPING_NOTIFICATION),
    (OrderTrackingNotificationType.ORDER_DELIVERED_NOTICE, MessageType.ORDER_DELIVERED_NOTIFICATION)
)

ORDER_NOTIFICATION_CORRESPONDING_EMAIL_TYPE_DICT = {tracking_type: message_type for tracking_type, message_type in
                                                    ORDER_NOTIFICATION_CORRESPONDING_EMAIL_TYPE_TUPLE}
