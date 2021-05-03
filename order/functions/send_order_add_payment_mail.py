import os

from django.contrib.auth import get_user_model

from admin_tools.constants import SystemSettingTypes
from admin_tools.models import MailSetting, SystemSetting
from notification.enums.message_types import MessageType
from notification.models import Template
from notification.services.notification import send_user_email
from order.models import Order

User = get_user_model()


def send_order_add_payment_mail(user_id, order_id, connection):
    user = User.objects.get(id=user_id)
    order = Order.objects.get(id=order_id)
    if not order.is_send_mail_add_payment:
        template = Template.objects.get(pk=MessageType.ADD_PAYMENT_EMAIL)
        client_site = os.environ.get("CLIENT_URL")
        base_order_url = "{}/u/orders/{}"
        order_link = base_order_url.format(client_site, order_id)
        email_data = {
            "user_name": user.name if user.name else user.email,
            "order_id": order_id,
            "order_link": order_link
        }
        setting = SystemSetting.objects.filter(type=SystemSettingTypes.AUTO_SEND_ADD_PAYMENT_NOTIFICATION).first().value
        bcc = setting.get('bcc')
        email_list = [user.email] if setting.get('send_to_user') else []
        success = send_user_email(user, template, email_data, email_list, send_html=True, connection=connection,
                                  bcc=bcc)
        if success:
            order.is_send_mail_add_payment = True
            order.save()
