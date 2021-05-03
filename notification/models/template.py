from django.db import models

from admin_tools.models.custom_mail_sender import CustomMailSender
from notification.enums.message_types import MESSAGE_TYPES, MessageType


class Template(models.Model):
    type = models.CharField(primary_key=True, max_length=2, choices=MESSAGE_TYPES,
                            default=MessageType.CANCEL_SHIPPING_APPROVED, blank=True)
    message_title = models.CharField(max_length=255, null=True, blank=True)
    message_content = models.CharField(max_length=2000, null=True, blank=True)
    mail_title = models.CharField(max_length=255, null=True, blank=True)
    mail_content = models.CharField(max_length=5000, null=True, blank=True)
    send_email = models.BooleanField(default=True, null=False)
    send_message = models.BooleanField(default=True, null=False)
    parameter_list = models.CharField(max_length=2000, null=True, blank=True)
    is_send_custom_mail = models.BooleanField(default=False)
    mail_sender = models.ForeignKey(CustomMailSender, on_delete=models.CASCADE, null=True, related_name='mail_sender')

    @property
    def verbose_type(self):
        current_type = self.type
        for type_choice in MESSAGE_TYPES:
            short_type, verbose_type = type_choice
            if short_type == current_type:
                return verbose_type

    class Meta:
        ordering = ["-type"]

    ATTRIBUTE_LABELS = [('message_title', 'Message Title'),
                        ('message_content', 'Message Content'),
                        ('mail_title', 'Mail Title'),
                        ('mail_content', 'Mail Content'),
                        ('send_email', 'Is Send Email'),
                        ('send_message', 'Is Send Message'),
                        ('parameter_list', 'Parameter List')]
