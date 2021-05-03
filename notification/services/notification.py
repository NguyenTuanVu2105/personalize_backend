import logging
from collections import defaultdict

from celery.decorators import task
from django.contrib.auth import get_user_model
from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils.html import strip_tags

from HUB import settings
from HUB.constants.celery_task import CeleryTask
from HUB.services.model_service import get_model_related_fields, AGGREGATE_FUNCTION_DICT
from admin_tools.models.mail_settings import MailSetting
from helper.datetime_helpers import get_current_datetime
from notification.enums.mail_history_statuses import MailHistoryStatus
from notification.enums.message_statuses import MessageStatus
from notification.models import Template, Message, MailHistory
from service_communication.constants.celery_log_action import CeleryLogAction
from service_communication.models import CeleryLog

User = get_user_model()

MAX_EMAIL_SEND_PER_NOTIFICATION = 3

logger = logging.getLogger(__name__)


@task(name=CeleryTask.TASK_SEND_NOTIFICATION)
def send_notification_task(user_id, message_type, data, email_list=None):
    return send_notification(user_id, message_type, data, email_list)


@task(name=CeleryTask.TASK_SEND_ADMIN_NOTIFICATION)
def send_admin_notification(message_type, data, emails=None, cc=None, bcc=None):
    try:
        users = User.objects.filter(is_superuser=True)
        template = Template.objects.get(pk=message_type)
        user_emails = emails or list(map(lambda user: user.email, users))
        if template.send_email:
            send_user_email(users[0], template, data, user_emails, cc=cc, bcc=bcc, send_html=True)
        if template.send_message:
            send_message(users[0], template, data)
    except Exception as e:
        logging.exception(e)


def send_notification(user_id, message_type, data, email_list=None, cc=None, bcc=None):
    try:
        user = User.objects.get(pk=user_id)
        template = Template.objects.get(pk=message_type)
        if template.send_email:
            send_user_email(user, template, data, email_list, cc=cc, bcc=bcc, send_html=True)
        if template.send_message:
            send_message(user, template, data)
    except Exception as e:
        logging.exception(e)


def get_connection_email(email, password):
    if email:
        return get_connection(host='smtp.gmail.com',
                              port=587,
                              username=email,
                              password=password,
                              use_tls=True)
    return None


def send_user_email(user, template, data, email_list=None, send_html=False, custom_email='', custom_password='',
                    connection=None, cc=None, bcc=None):
    if 'mail_title_include' in data:
        title = template.mail_title.format(mail_title_include=data['mail_title_include'])
    else:
        title = template.mail_title.format_map(defaultdict(str, **data))
    if 'mail_content_include' in data:
        content = template.mail_content.format(mail_content_include=data['mail_content_include'])
    else:
        content = template.mail_content.format_map(defaultdict(str, **data))

    emails = email_list[:MAX_EMAIL_SEND_PER_NOTIFICATION] if email_list is not None else [user.email]
    mail_history = MailHistory(owner=user, email=";".join(emails), type=template.type, status=MailHistoryStatus.PENDING)
    try:
        if send_html:
            plain_text = strip_tags(content)
            send_mail(title, plain_text, settings.EMAIL_SENDER, emails, connection=connection, html_message=content,
                      cc=cc, bcc=bcc)
        else:
            send_mail(title, content, settings.EMAIL_SENDER, emails, connection=connection, cc=cc, bcc=bcc)
        mail_history.send_time = get_current_datetime()
        mail_history.status = MailHistoryStatus.SENT
    except Exception as e:
        logging.exception(e)
        mail_history.status = MailHistoryStatus.ERROR
    mail_history.save()
    return mail_history.status == MailHistoryStatus.SENT


def send_user_email_with_setting(user, template, data, email_list=None, send_html=False, cc=None, bcc=None):
    mail_setting = MailSetting.objects.first()
    email_list = email_list.append(mail_setting.admin_mail) if email_list else [mail_setting.admin_mail]
    email_list.append(user.email)
    if mail_setting.is_send_mail_user:
        send_user_email(user, template, data, email_list, send_html, cc=cc, bcc=bcc)


def send_custom_email(receivers, title, content, data, send_as_html=True, cc=None, bcc=None):
    data = data or {'subject': {}, 'content': {}}
    title = title.format(**(data.get('subject') or {}))
    content = content.format(**(data.get('content') or {}))
    if send_as_html:
        plain_text = strip_tags(content)
        return send_mail(title, plain_text, settings.EMAIL_SENDER, receivers, html_message=content, cc=cc, bcc=bcc)
    else:
        return send_mail(title, content, settings.EMAIL_SENDER, receivers, cc=cc, bcc=bcc)


def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None, cc=None, bcc=None):
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection, cc=cc, bcc=bcc)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')

    return mail.send()


@task(name=CeleryTask.TASK_SEND_SELLER_CUSTOM_EMAIL)
def send_seller_custom_email_task(receiver_emails, subject, content, data_mapping):
    process_log = {'success': [], 'fail': [], 'error': [], 'ignore': []}
    for email in receiver_emails:
        receiver = User.objects.filter(email=email).first()
        if receiver.is_test_user:
            process_log['ignore'].append(email)
            continue
        email_data = {'subject': {}, 'content': {}}
        subject_data_mapping = data_mapping.get('subject')
        if subject_data_mapping:
            for field, field_data in subject_data_mapping.items():
                aggregate_name = field_data.get('aggregate')
                if aggregate_name:
                    aggregate_name = aggregate_name.lower()
                email_data['subject'][field] = get_model_related_fields(receiver, field_data['related_field'],
                                                                        aggregate_name or None)
        content_data_mapping = data_mapping.get('content')
        if content_data_mapping:
            for field, field_data in content_data_mapping.items():
                email_data['content'][field] = get_model_related_fields(receiver, field_data['related_field'],
                                                                        AGGREGATE_FUNCTION_DICT.get(
                                                                            field_data.get('aggregate')) or None)
        try:
            success = send_custom_email([email], subject, content, email_data)
            if success:
                process_log['success'].append(email)
            else:
                process_log['fail'].append(email)
        except Exception as e:
            logger.exception(e)
            process_log['error'].append(email)
    CeleryLog.objects.create(action=CeleryLogAction.SEND_EMAIL, note=process_log)


def send_message(user, template, data):
    from notification.services import set_num_unread_msg
    title = template.message_title.format(**data)
    content = template.message_content.format(**data)
    message = Message(owner=user, type=template.type, title=title, content=content, status=MessageStatus.UNREAD)
    message.save()
    set_num_unread_msg(user, Message.objects.filter(owner=user, status=MessageStatus.UNREAD).count())
