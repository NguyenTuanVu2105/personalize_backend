from django.contrib.postgres.fields import JSONField
from django.db import models

from admin_tools.constants import SYSTEM_SETTING_TYPE_CHOICES


class SystemSetting(models.Model):
    type = models.CharField(primary_key=True, choices=SYSTEM_SETTING_TYPE_CHOICES, max_length=2)
    name = models.CharField(max_length=256, null=True)
    value = JSONField(default={})

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)

    @property
    def verbose_type(self):
        current_type = self.type
        for type_choice in SYSTEM_SETTING_TYPE_CHOICES:
            short_type, verbose_type = type_choice
            if short_type == current_type:
                return verbose_type

    class Meta:
        db_table = 'system_setting'
