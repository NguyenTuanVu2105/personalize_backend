from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from abstract_product.models import AbstractProductSide
from user_product.constants import ArtworkStatus, ARTWORK_STATUS_CHOICES

User = get_user_model()


class ArtworkDefault(RandomIDModel):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='artwork_default_set',
                              verbose_name=_('Owner Artwork Default'))
    product_side = models.ForeignKey(AbstractProductSide, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='artwork_default_product_side',
                                     verbose_name=_('Abstract Product Side'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    file_url = models.TextField(verbose_name=_('Artwork Default Thumbnail Url'))
    original_image_path = models.TextField(verbose_name=_('Storage Artwork Default Path'))
    thumbnail_image_path = models.TextField(verbose_name=_('Thumbnail Storage Artwork Default Path'), null=True)
    width = models.IntegerField(default=0, db_index=True)
    height = models.IntegerField(default=0, db_index=True)
    status = models.CharField(max_length=16, default=ArtworkStatus.ACTIVE, choices=ARTWORK_STATUS_CHOICES,
                              db_index=True)
    sha256 = models.CharField(max_length=270, null=True, blank=True)
    is_public = models.BooleanField(default=False, db_index=True)
    total_created_product = models.IntegerField(default=0)
    last_used_time = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)
    product_sku = models.CharField(max_length=20, null=True, blank=True)
    is_legal_accepted = models.BooleanField(default=True)

    tsv_metadata_search = SearchVectorField(null=True)

    class Meta:
        db_table = 'artwork_default'
        ordering = ['id']
        verbose_name = _('Artwork Default')
        verbose_name_plural = _('Artworks Default')
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    def __str__(self):
        return self.name

    def parse_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "file_url": self.file_url,
            "width": self.width,
            "height": self.height,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

    def generate_original_image_signed_url(self):
        from HUB.services import gs_image_service
        storage_artwork_path = gs_image_service.convert_private_file_path_to_signed_url(self.original_image_path)
        return storage_artwork_path
