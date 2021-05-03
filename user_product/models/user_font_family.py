from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel

User = get_user_model()


class UserFontFamily(RandomIDModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    font_url = models.TextField(null=True)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='font_family_set', verbose_name=_('User'))
    is_active = models.BooleanField(default=True)
    available_characters = JSONField(default=list)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'user_product__user_font_family'
        ordering = ['title']
        verbose_name = _('User Font Family')
        verbose_name_plural = _('User Fonts Family')

    @property
    def used_frequency(self):
        return self.text_personalization_set.count()

    def __str__(self):
        return _("Font: {} | Owner: {}".format(self.title, self.owner))
