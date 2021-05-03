from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from .user_variant import UserVariant


class UserVariantSideMockup(RandomIDModel):
    user_variant = models.ForeignKey(UserVariant, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='mockup_per_side', verbose_name=_('User Variant'))
    mockup_url = models.TextField(verbose_name=_('Mockup Url'))
    mockup_thumbnail_url = models.TextField(verbose_name=_('Mockup Thumbnail Url'))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_variant_side_mockup'
        ordering = ['update_time', 'create_time']
        verbose_name = _('User Variant Side Mockup')
        verbose_name_plural = _('User Variant Side Mockups')

    def __str__(self):
        return _("User Variant: {}".format(self.user_variant))

    def parse_info(self):
        info = {
            "user_variant": self.user_variant.id,
            "mockup_url": self.mockup_url
        }
        return info
