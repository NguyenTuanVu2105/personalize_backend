from django.contrib.postgres.fields import JSONField
from django.db import models

from service_communication.constants.schedule_type import SCHEDULE_TYPES, ScheduleType


class ScheduleInfo(models.Model):
    schedule_type = models.CharField(max_length=10, choices=SCHEDULE_TYPES, unique=True,
                                     default=ScheduleType.AUTO_SCAN_SUPPORT_TICKET, db_index=True)
    meta = JSONField(default={})
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'service_communication_schedule_info'
