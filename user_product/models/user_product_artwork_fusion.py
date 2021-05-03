from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from abstract_product.models.abstract_product_side import AbstractProductSide
from .artwork_fusion import ArtworkFusion
from .user_product import UserProduct
from ..manager import UserProductArtworkFusionManager


class UserProductArtworkFusion(RandomIDModel):
    user_product = models.ForeignKey(UserProduct, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='artwork_set', verbose_name=_('User Product'))
    product_side = models.ForeignKey(AbstractProductSide, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='user_set', verbose_name=_('Abstract Product Side'))
    artwork_fusion = models.ForeignKey(ArtworkFusion, on_delete=models.SET_NULL,
                                       related_name='user_product_artwork_fusion_set', blank=True, null=True,
                                       verbose_name=_('Artwork Fusion'))

    send_to_fulfill = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = UserProductArtworkFusionManager()

    class Meta:
        db_table = 'user_product_artwork_fusion'
        ordering = ['id']
        unique_together = ('user_product', 'product_side', 'artwork_fusion')
        verbose_name = _('User Product Artwork')
        verbose_name_plural = _('User Product Artworks')

    @property
    def is_seller_visible(self):
        if self.user_product.combine_fusion:
            return not self.send_to_fulfill
        else:
            return self.send_to_fulfill

    def __str__(self):
        return _("User Product: {} | Side: {}".format(self.user_product, self.product_side.type))

    def parse_data_for_artwork_pushing(self):
        result = {
            "side": self.product_side.type.lower(),
            "url": self.artwork_fusion.generate_original_image_signed_url()
        }
        return result
