from admin_tools.constants import SystemSettingTypes
from admin_tools.models import SystemSetting
from order.models import Order
from order.tasks.send_order_review_mail_task import send_order_review_mail_task
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)
date_format = "%d-%m-%Y"

def scan_and_send_mail_review_orders():
    setting = SystemSetting.objects.filter(type=SystemSettingTypes.AUTO_SEND_ORDER_REVIEW).first().value
    if setting['auto_send']:
        schedule_start_time = pytz.utc.localize(datetime.strptime(setting['schedule_start_time'], date_format))
        orders = Order.objects.filter(is_delivered_order=True, update_time__gt=schedule_start_time)
        list_user_send_mail = []
        list_user_orders = []
        for order in orders:
            user_id = order.shop.owner.id
            if user_id not in list_user_send_mail:
                list_user_send_mail.append(user_id)
                list_user_orders.append((user_id, order.id))
        list_user_orders = [list_user_orders[i:i + 10] for i in range(0, len(list_user_orders), 10)]
        for user_order in list_user_orders:
            send_order_review_mail_task.delay(user_order)