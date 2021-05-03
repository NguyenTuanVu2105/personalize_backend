from datetime import datetime

import pytz

from admin_tools.constants import SystemSettingTypes
from admin_tools.models import MailSetting, SystemSetting
from order.constants.financial_statuses import OrderFinancialStatus
from order.models import Order
from order.tasks.send_order_not_add_payment_task import send_order_not_add_payment_task

import logging
logger = logging.getLogger(__name__)
date_format = "%d-%m-%Y"

def scan_and_send_mail_add_payment():
    setting = SystemSetting.objects.filter(type=SystemSettingTypes.AUTO_SEND_ADD_PAYMENT_NOTIFICATION).first().value
    if setting['auto_send']:
        schedule_start_time = pytz.utc.localize(datetime.strptime(setting['schedule_start_time'], date_format))
        orders = Order.objects.filter(financial_status=OrderFinancialStatus.FAILED, shop__owner__is_valid_payment=False, shop__owner__is_test_user=False, update_time__gt=schedule_start_time)
        list_user_send_mail = []
        list_user_orders = []
        for order in orders:
            user_id = order.shop.owner.id
            if user_id not in list_user_send_mail:
                list_user_send_mail.append(user_id)
                list_user_orders.append((user_id, order.id))
        # if not order.is_send_mail_add_payment:
        list_user_orders = [list_user_orders[i:i + 10] for i in range(0, len(list_user_orders), 10)]
        for user_order in list_user_orders:
            send_order_not_add_payment_task.delay(user_order)