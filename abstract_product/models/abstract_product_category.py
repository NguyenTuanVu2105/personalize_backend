from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
from HUB.models.random_id_model import RandomIDModel


class AbstractProductCategory(RandomIDModel):
    title = models.CharField(max_length=100, verbose_name=_('Title'), db_index=True)
    preview_image_url = models.CharField(max_length=512, null=True, verbose_name=_('Preview Image Url'))
    sort_index = models.IntegerField()
    is_active = models.BooleanField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    force_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'abstract_product_category'
        ordering = ['id']
        verbose_name = _('Abstract Product Category')
        verbose_name_plural = _('Abstract Product Categories')

    def __str__(self):
        return self.title

    def parse_data(self):
        data = {
            'id': self.id,
            'title': self.title,
            'preview_image_url': self.preview_image_url,
            'is_active': self.is_active,
            'update_time': self.update_time,
            'create_time': self.create_time,
            'sort_index': self.sort_index
        }
        return data

    def parse_basic_info(self):
        data = {
            'id': self.id,
            'title': self.title,
            'preview_image_url': self.preview_image_url,
        }
        return data
