from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB import settings
from HUB.models.random_id_model import RandomIDModel
from notification.enums.instant_prompt_types import INSTANT_PROMPT_TYPES, InstantPromptType, INSTANT_PROMPT_TYPE_DICT
from notification.enums.message_statuses import MESSAGE_STATUSES, MessageStatus, MESSAGE_STATUS_DICT


class InstantPrompt(RandomIDModel):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=INSTANT_PROMPT_TYPES,
                            default=InstantPromptType.ADD_PAYMENT_METHOD, blank=True, db_index=True)
    params = JSONField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=MESSAGE_STATUSES,
                              default=MessageStatus.UNREAD, blank=True)

    @property
    def verbose_status(self):
        return MESSAGE_STATUS_DICT.get(self.status)

    @property
    def verbose_type(self):
        return INSTANT_PROMPT_TYPE_DICT.get(self.type)

    class Meta:
        ordering = ["-create_time"]
        # unique_together = ('owner', 'type')
