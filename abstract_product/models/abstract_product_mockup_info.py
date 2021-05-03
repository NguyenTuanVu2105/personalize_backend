from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from abstract_product.models import AbstractProduct


def default_meta():
    return {
        "mockup_infos": [{
            "width": 1000,
            "height": 1000,
            "frame_width": 200,
            "frame_height": 150,
            "frame_x": 150,
            "frame_y": 150,
            "image_path": "",
            "type": "transparent",
            "side": "front"
        }],
    }


def default_preview():
    return {
               "front": {
                   "image_width": 1000,
                   "image_height": 1000,
                   "frame_width": 212,
                   "frame_height": 227,
                   "frame_x": 212,
                   "frame_y": 227,
                   "image_path": ""
               }
           },


def default_preview_meta():
    return {
               "enable_preview": 1,
               "z_index": 3
           },


class AbstractProductMockupInfo(RandomIDModel):
    abstract_product = models.ForeignKey(AbstractProduct, on_delete=models.CASCADE, related_name='mockup_infos')
    name = models.CharField(max_length=50, default='', null=True, blank=True)
    meta = JSONField(default=default_meta)
    preview = JSONField(default=default_preview)
    preview_meta = JSONField(default=default_preview_meta())
    # enable_preview = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'abstract_product_mockup_info'
        ordering = ['id']
        verbose_name = _('Abstract Product Mockup Info')
        verbose_name_plural = _('Abstract Product Mockup Info')
