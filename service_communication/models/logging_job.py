from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from service_communication.constants.celery_log_action import CeleryLogActionChoices


class CeleryLog(RandomIDModel):
    action = models.CharField(max_length=1, choices=CeleryLogActionChoices)
    note = JSONField(default={})
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id', 'create_time']
        db_table = 'service_communication_celery_log'
