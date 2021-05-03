from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB import CeleryTask
from admin_tools.constants import SystemSettingTypes
from admin_tools.models import SystemSetting
from notification.services.notification import get_connection_email
from order.functions.send_order_add_payment_mail import send_order_add_payment_mail

logger = get_task_logger(__name__)

@task(name=CeleryTask.TASK_CREATE_ADD_PAYMENT_MAIL)
def send_order_not_add_payment_task(list_user_orders):
    logger.info("Send add payment mail")
    setting = SystemSetting.objects.filter(type=SystemSettingTypes.AUTO_SEND_ORDER_REVIEW).first().value
    connection = get_connection_email(setting['custom_sender']['email'], setting['custom_sender']['password'])
    for list_user_order in list_user_orders:
        user_id, order_id = list_user_order
        send_order_add_payment_mail(user_id, order_id, connection)