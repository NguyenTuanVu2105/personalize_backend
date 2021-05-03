from django.db import models

from HUB import settings
from HUB.models.random_id_model import RandomIDModel
from notification.enums.mail_history_statuses import MAIL_HISTORY_STATUSES, MailHistoryStatus
from notification.enums.message_types import MESSAGE_TYPES, MessageType


class MailHistory(RandomIDModel):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=MESSAGE_TYPES,
                            default=MessageType.CANCEL_SHIPPING_APPROVED, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    send_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=2, choices=MAIL_HISTORY_STATUSES,
                              default=MailHistoryStatus.PENDING, blank=True)

    @property
    def verbose_status(self):
        current_status = self.status
        for status_choice in MAIL_HISTORY_STATUSES:
            short_status, verbose_status = status_choice
            if short_status == current_status:
                return verbose_status

    @property
    def verbose_type(self):
        current_type = self.type
        for type_choice in MESSAGE_TYPES:
            short_type, verbose_type = type_choice
            if short_type == current_type:
                return verbose_type

    class Meta:
        ordering = ["-create_time"]
