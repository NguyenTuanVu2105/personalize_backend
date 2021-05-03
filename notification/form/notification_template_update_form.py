from HUB.forms.base import ModelForm
from notification.models import Template

ALLOW_UPDATE_FIELDS = ["message_title", "message_content", "mail_title", "mail_content", "send_email", "send_message", "parameter_list", "is_send_custom_mail", "mail_sender"]


class NotificationTemplateUpdateForm(ModelForm):
    class Meta:
        model = Template
        fields = ALLOW_UPDATE_FIELDS
        optional_fields = ALLOW_UPDATE_FIELDS
