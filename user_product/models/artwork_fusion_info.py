from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from user_product.constants import default_position, default_scale, default_rotation
from .artwork import Artwork
from .artwork_fusion import ArtworkFusion
from ..constants.artwork_fusion_info_metas import LAYER_TYPE_CHOICES
from ..manager import ArtworkFusionInfoManager

User = get_user_model()


class ArtworkFusionInfo(RandomIDModel):
    # artwork = models.ForeignKey(Artwork, on_delete=models.SET_NULL, blank=True, null=True,
    #                             related_name='artwork_fusion_info_frame_set',
    #                             verbose_name=_('Artwork'))
    frame = models.ForeignKey(ArtworkFusion, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='artwork_fusion_info_artwork_set',
                              verbose_name=_('Artwork Fusion'))
    layer = models.SmallIntegerField(default=1)
    rotation = models.DecimalField(max_digits=5, decimal_places=2, default=default_rotation)
    position = JSONField(default=default_position)
    scale = models.DecimalField(max_digits=6, decimal_places=3, default=default_scale)
    dnd_scale = models.DecimalField(max_digits=6, decimal_places=3, default=default_scale)
    is_hidden = models.BooleanField(default=False)

    layer_type = models.CharField(max_length=50, choices=LAYER_TYPE_CHOICES)
    layer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    layer_content_id = models.BigIntegerField(null=True)
    layer_content = GenericForeignKey('layer_content_type', 'layer_content_id')

    objects = ArtworkFusionInfoManager()

    class Meta:
        db_table = 'artwork_fusion_info'
        ordering = ['layer']
        verbose_name = _('Artwork Fusion Info')
        verbose_name_plural = _('Artwork Fusion Infos')

    # @property
    # def layer_type(self):
    #     return self.layer_content_type.model

    def __str__(self):
        return "Artwork Fusion Info: Frame {} | Layer Content {}".format(self.frame.name, self.layer_content)
