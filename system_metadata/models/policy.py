from django.db import models
from django.utils.translation import gettext as _


class Policy(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    last_updated_content = models.TextField(null=True, blank=True)
    sort_index = models.SmallIntegerField(default=0, verbose_name='Sort Index')
    is_prompt = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'system_meta_policy'
        ordering = ['sort_index']
        verbose_name = _('Policy')
        verbose_name_plural = _('Policies')

    def __str__(self):
        return "Policy: {}".format(self.title)
