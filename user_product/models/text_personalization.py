from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from user_product.constants import DEFAULT_PERSONAL_TEXT_PLACEHOLDER, DEFAULT_TEXT_COLOR, DEFAULT_TEXT_SIZE, \
    DEFAULT_TEXT_SPACING, DEFAULT_ARC, DEFAULT_ALLOW_CUSTOMIZE


class TextPersonalization(RandomIDModel):
    placeholder_label = models.CharField(max_length=64, default=DEFAULT_PERSONAL_TEXT_PLACEHOLDER, blank=True)
    raw_svg = models.TextField(null=False, blank=False)
    is_allow_customize = models.BooleanField(default=DEFAULT_ALLOW_CUSTOMIZE)

    text = models.CharField(max_length=255, blank=True)
    font_family = models.ForeignKey('user_product.UserFontFamily', on_delete=models.CASCADE,
                                    related_name='text_personalization_set', verbose_name=_('Font'))
    text_color = models.CharField(max_length=10, default=DEFAULT_TEXT_COLOR, verbose_name=_('Text Color'))
    text_size = models.IntegerField(default=DEFAULT_TEXT_SIZE, verbose_name=_('Text Size'))
    text_spacing = models.IntegerField(default=DEFAULT_TEXT_SPACING, verbose_name=_('Text Spacing'))
    outline_color = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Outline Color'))
    outline_thickness = models.IntegerField(null=True, blank=True, verbose_name=_('Outline Thickness'))
    shadow_color = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Shadow Color'))
    shadow_distance = models.IntegerField(null=True, blank=True, verbose_name=_('Shadow Distance'))
    shadow_angle = models.FloatField(null=True, blank=True, verbose_name=_('Shadow Angle'))
    arc = models.IntegerField(default=DEFAULT_ARC, verbose_name=_('Arc'))

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_product__text_personalization'
        ordering = ['id']
        verbose_name = _('Text Personalization')
        verbose_name_plural = _('Texts Personalization')

    def __str__(self):
        return _("Text Personalization: {} | Label: {}".format(self.id, self.placeholder_label))
