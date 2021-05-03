from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel


class ArtworkHistory(RandomIDModel):
    original_artwork = models.ForeignKey(to="user_product.Artwork", on_delete=models.SET_NULL, blank=True, null=True,
                                         related_name='artwork_history_set',
                                         verbose_name=_('Origin Artwork'))
    original_name = models.CharField(max_length=100, verbose_name=_('Name'))
    original_image_url = models.TextField(verbose_name=_('Storage Artwork Url'))
    original_width = models.IntegerField(default=0)
    original_height = models.IntegerField(default=0)
    sha256 = models.CharField(max_length=270)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'artwork_history'
        ordering = ['-create_time']
        verbose_name = _('Artwork History')
        verbose_name_plural = _('Artwork Histories')

    def __str__(self):
        return "Artwork History: {}".format(self.original_name)

    def parse_data(self):
        return {
            "id": self.id,
            "origin_artwork": self.original_artwork.__str__(),
            "origin_name": self.original_name,
            "original_image_url": self.original_image_url,
            "name": self.original_name,
            "create_time": self.create_time,
        }

    # def generate_original_image_signed_url(self):
    #     from HUB.services import gs_image_service
    #     storage_artwork_path = gs_image_service.convert_private_file_path_to_signed_url(self.original_image_path)
    #     return storage_artwork_path
