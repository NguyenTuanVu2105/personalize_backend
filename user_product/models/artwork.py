from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from user_product.constants import ARTWORK_STATUS_CHOICES, ArtworkStatus
# from user_product.functions.storage import artwork_image_service
# from .artwork_history import ArtworkHistory
from user_product.models.artwork_default import ArtworkDefault

User = get_user_model()


class Artwork(RandomIDModel):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='artwork_set',
                              verbose_name=_('Owner'))
    artwork_default = models.ForeignKey(ArtworkDefault, on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name='artwork_default',
                                        verbose_name=_('Artwork default'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    file_url = models.TextField(verbose_name=_('Artwork Thumbnail Url'))
    original_image_path = models.TextField(verbose_name=_('Storage Artwork Path'))
    thumbnail_image_path = models.TextField(verbose_name=_('Thumbnail Storage Artwork Path'), null=True)
    width = models.IntegerField(default=0, db_index=True)
    height = models.IntegerField(default=0, db_index=True)
    is_public = models.BooleanField(default=False, db_index=True)
    # is_active = models.BooleanField(default=True, db_index=True)
    status = models.CharField(max_length=16, default=ArtworkStatus.UPLOADED, choices=ARTWORK_STATUS_CHOICES,
                              db_index=True)
    sha256 = models.CharField(max_length=270, null=True, blank=True)

    last_used_time = models.DateTimeField(db_index=True)
    total_created_product = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)
    is_legal_accepted = models.BooleanField(default=False)
    fusion_info = GenericRelation(to='user_product.ArtworkFusionInfo', content_type_field='layer_content_type',
                                  object_id_field='layer_content_id')

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)

    tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = 'artwork'
        ordering = ['id']
        verbose_name = _('Artwork')
        verbose_name_plural = _('Artworks')
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    def __str__(self):
        return self.name

    def parse_data(self):
        return {
            "id": self.id,
            "owner": self.owner.__str__(),
            "name": self.name,
            "file_url": self.file_url,
            "is_active": self.status,
            "is_public": self.is_public,
            "width": self.width,
            "height": self.height,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }

    def generate_original_image_signed_url(self):
        from HUB.services import gs_image_service
        storage_artwork_path = gs_image_service.convert_private_file_path_to_signed_url(self.original_image_path)
        return storage_artwork_path

    # def create_artwork_history(self):
    #     ArtworkHistory.objects.create(original_artwork=self, original_image_url=self.file_url, original_name=self.name,
    #                                   sha256=self.sha256)

    # def delete_artwork(self, self_delete=True):
    #     artwork_image_service.delete_original_image(self.original_image_path)
    #     artwork_image_service.delete_thumnail_image(self.thumbnail_image_path)
    #     if self_delete:
    #         self.delete()
    #     return None
