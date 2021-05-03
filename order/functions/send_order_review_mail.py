import os

from django.contrib.auth import get_user_model

from admin_tools.constants import SystemSettingTypes
from admin_tools.models import SystemSetting
from notification.enums.message_types import MessageType
from notification.models import Template
from notification.services.notification import send_user_email
from order.functions.is_send_order_review_mail import is_send_order_review_mail

User = get_user_model()


def send_order_review_mail(user_id, order_id, connection):
    user = User.objects.get(id=user_id)
    template = Template.objects.get(pk=MessageType.ORDER_DELIVERED_REVIEW)
    client_site = os.environ.get("CLIENT_URL")
    base_order_url = "{}/u/orders/{}"
    order_link = base_order_url.format(client_site, order_id)
    email_data = {
        "user_name": user.name if user.name else user.email,
        "order_id": order_id,
        "order_link": order_link
    }
    setting = SystemSetting.objects.filter(type=SystemSettingTypes.AUTO_SEND_ORDER_REVIEW).first().value
    bcc = setting.get('bcc')
    email_list = [user.email] if setting.get('send_to_user') else []
    if is_send_order_review_mail(user_id):
        send_user_email(user, template, email_data, email_list=email_list, send_html=True, connection=connection,
                        bcc=bcc)
