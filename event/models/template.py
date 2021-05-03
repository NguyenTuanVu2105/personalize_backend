from django.db import models

from HUB.models.random_id_model import RandomIDModel
from event.constants.event_template_status import EVENT_TEMPLATE_STATUS, EventTemplateStatus


class EventTemplate(RandomIDModel):
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(choices=EVENT_TEMPLATE_STATUS, max_length=2, default=EventTemplateStatus.ACTIVE,
                              db_index=True)
    header_html = models.CharField(max_length=3000)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event_template'
        ordering = ['id']
