from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from .artwork import Artwork

User = get_user_model()


class ArtworkFusion(RandomIDModel):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='artwork_fusion_set',
                              verbose_name=_('Owner'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    original_image_path = models.TextField(verbose_name=_('Storage Artwork Fusion Path'), null=True)
    image_url = models.TextField(verbose_name=_('Storage Artwork Fusion Url'), null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)
    background_color = models.CharField(max_length=7, null=True, blank=True, default=None)
    last_fusion_update_time = models.DateTimeField(db_index=True, null=True)

    class Meta:
        db_table = 'artwork_fusion'
        ordering = ['id']
        verbose_name = _('Artwork Fusion')
        verbose_name_plural = _('Artwork Fusions')

    def __str__(self):
        return self.name

    def parse_data(self):
        return {
            "id": self.id,
            "owner": self.owner.__str__(),
            "name": self.name,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

    def generate_original_image_signed_url(self):
        from HUB.services import gs_image_service
        storage_artwork_path = gs_image_service.convert_private_file_path_to_signed_url(self.original_image_path)
        return storage_artwork_path
