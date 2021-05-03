from admin_tools.constants import SystemSettingTypes
from admin_tools.models.system_settings import SystemSetting
from notification.constants import OrderTrackingNotificationType
from notification.models.order_notification import OrderTrackingNotification
from order.models import Order


def create_order_tracking_notification(order_id, notification_type, receive_email):
    created_obj, created = OrderTrackingNotification.objects \
        .get_or_create(order_id=order_id,
                       receive_email=receive_email,
                       type=notification_type)
    return created_obj


def create_order_shipping_notification(order_id):
    pass
    # setting = SystemSetting.objects.get(type=SystemSettingTypes.AUTO_SEND_SHIPPING_ORDER_NOTIFICATION)\
    #     .value
    # if not setting.get('auto_create'):
    #     return
    # order = Order.objects.get(id=order_id)
    # receive_email = order.shop.owner.email
    # if order.is_shipping():
    #     return create_order_tracking_notification(order_id,
    #                                               OrderTrackingNotificationType.ORDER_SHIPPING_NOTICE,
    #                                               receive_email)


def create_order_delivered_notification(order_id):
    setting = SystemSetting.objects.get(type=SystemSettingTypes.AUTO_SEND_DELIVERED_ORDER_NOTIFICATION)\
        .value
    if not setting.get('auto_create'):
        return
    admin_email = setting.get('default_admin_email')
    order = Order.objects.get(id=order_id)
    if order.is_delivered() and admin_email:
        return create_order_tracking_notification(order_id,
                                                  OrderTrackingNotificationType.ORDER_DELIVERED_NOTICE,
                                                  admin_email)
