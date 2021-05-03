from datetime import datetime

from admin_tools.constants import SystemSettingTypes
from admin_tools.models.system_settings import SystemSetting
from notification.constants import ORDER_NOTIFICATION_CORRESPONDING_EMAIL_TYPE_DICT, \
    OrderTrackingNotificationType
from notification.models import OrderTrackingNotification, Template
from notification.services.notification import send_user_email


def handle_unsent_order_tracking_notification():
    unsent_notifications = OrderTrackingNotification.objects.filter(sent_time__isnull=True)

    # auto_send_shipping_notification_setting = SystemSetting.objects \
    #     .get(type=SystemSettingTypes.AUTO_SEND_SHIPPING_ORDER_NOTIFICATION) \
    #     .value
    # send_list = unsent_notifications.filter(type=OrderTrackingNotificationType.ORDER_SHIPPING_NOTICE)
    # bulk_send_order_tracking_notifications(send_list,
    #                                        auto_send_shipping_notification_setting.get('receive_email_cc'))
    auto_send_delivered_notification_setting = SystemSetting.objects \
        .get(type=SystemSettingTypes.AUTO_SEND_DELIVERED_ORDER_NOTIFICATION) \
        .value
    send_list = unsent_notifications.filter(type=OrderTrackingNotificationType.ORDER_DELIVERED_NOTICE)
    bulk_send_order_tracking_notifications(send_list,
                                           auto_send_delivered_notification_setting.get('receive_email_cc'))


def bulk_send_order_tracking_notifications(notifications, receive_email_cc=None):
    receive_email_cc = receive_email_cc or None
    for notification in notifications:
        send_order_tracking_notification(notification, receive_email_cc)
        notification.sent_time = datetime.now()
        notification.save()


def send_order_tracking_notification(order_tracking_notification, receive_email_cc=None):
    user = order_tracking_notification.order.shop.owner
    template = Template.objects.get(
        type=ORDER_NOTIFICATION_CORRESPONDING_EMAIL_TYPE_DICT[order_tracking_notification.type])
    data = {'order_id': order_tracking_notification.order.id}
    email_list = [order_tracking_notification.receive_email, ]
    send_html = True
    send_user_email(user, template, data, email_list, send_html, cc=receive_email_cc)
