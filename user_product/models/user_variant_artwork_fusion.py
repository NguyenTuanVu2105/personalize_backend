from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from abstract_product.models.abstract_product_side import AbstractProductSide
from . import UserVariant
from .artwork_fusion import ArtworkFusion


class UserVariantArtworkFusion(RandomIDModel):
    user_variant = models.ForeignKey(UserVariant, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='user_variant_artwork_set', verbose_name=_('User Variant'))
    variant_side = models.ForeignKey(AbstractProductSide, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='variant_side_set', verbose_name=_('Abstract Product Side'))
    artwork_fusion = models.ForeignKey(ArtworkFusion, on_delete=models.SET_NULL,
                                       related_name='user_variant_artwork_fusion_set', blank=True, null=True,
                                       verbose_name=_('Artwork Fusion'))

    class Meta:
        db_table = 'user_variant_artwork_fusion'
        ordering = ['id']
        unique_together = ('user_variant', 'variant_side', 'artwork_fusion')
        verbose_name = _('User Product Artwork')
        verbose_name_plural = _('User Product Artworks')

    def __str__(self):
        return _("User Variant: {} | Side: {}".format(self.user_variant, self.variant_side.type))

    def parse_data_for_artwork_pushing(self):
        result = {
            "side": self.variant_side.type,
            "url": self.artwork_fusion.generate_original_image_signed_url()
        }
        return result
