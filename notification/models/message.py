from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB import settings
from HUB.models.random_id_model import RandomIDModel
from notification.enums.message_statuses import MESSAGE_STATUSES, MessageStatus
from notification.enums.message_types import MessageType, MESSAGE_TYPES


class Message(RandomIDModel):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=MESSAGE_TYPES,
                            default=MessageType.CANCEL_SHIPPING_APPROVED, blank=True)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=2000)
    params = JSONField(default={})
    create_time = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=MESSAGE_STATUSES,
                              default=MessageStatus.UNREAD, blank=True)

    @property
    def verbose_status(self):
        current_status = self.status
        for status_choice in MESSAGE_STATUSES:
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
