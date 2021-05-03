from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from .abstract_product import AbstractProduct


def default_constraints():
    return {
        "allowed_sizes": [],
        "minimum_dpi": 300
    }


def default_fusion_size():
    return {
        "artwork_fusion_size": {
            "width": 0,
            "height": 0,
            "width_in_inch": 0,
            "height_in_inch": 0
        },
        "edit_artwork_fusion_size": {
            "width": 0,
            "height": 0,
            "width_in_inch": 0,
            "height_in_inch": 0
        }
    }


class AbstractProductSide(RandomIDModel):
    abstract_product = models.ForeignKey(AbstractProduct, on_delete=models.CASCADE, related_name='sides', null=True)
    type = models.CharField(max_length=50)
    constraints = JSONField(default=default_constraints)
    fusion_size = JSONField(default=default_fusion_size)
    enable_background_color = models.BooleanField(default=False)
    fulfill_require_artwork = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'abstract_product_side'
        ordering = ['id']
        unique_together = ('abstract_product', 'type')
        verbose_name = _('Abstract Product Side')
        verbose_name_plural = _('Abstract Product Side')

    def __str__(self):
        return self.type
