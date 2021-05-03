from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel


class SKUTemplate(RandomIDModel):
    sku = models.CharField(max_length=255, verbose_name=_('SKU'), unique=True)
    png_template_url = models.TextField()

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'abstract_product__sku_template'
        ordering = ['sku']
        verbose_name = _('SKU Template')
        verbose_name_plural = _('SKU Templates')

    def __str__(self):
        return self.sku
