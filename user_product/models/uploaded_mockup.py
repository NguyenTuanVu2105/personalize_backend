from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel

User = get_user_model()


class UploadedMockup(RandomIDModel):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='uploaded_mockups',
                              verbose_name=_('Owner'))
    file_url = models.TextField(verbose_name=_('Artwork Thumbnail Url'))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'user_product__uploaded_mockup'
        ordering = ['-create_time']
        verbose_name = _('Uploaded Mockup')
        verbose_name_plural = _('Uploaded Mockups')

    def __str__(self):
        return "Owner: {} | Url: {}".format(self.owner, self.file_url)