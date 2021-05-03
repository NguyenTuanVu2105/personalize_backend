from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from .abstract_product import AbstractProduct


class ProductAttribute(RandomIDModel):
    product = models.ForeignKey(AbstractProduct, on_delete=models.CASCADE, blank=True, null=True, related_name='child_attributes', verbose_name=_('Product'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    type = models.CharField(max_length=31, verbose_name=_('Select Type'))
    sort_index = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'abstract_product_attribute'
        ordering = ['sort_index', 'name']
        unique_together = ('product', 'name')
        verbose_name = _('Product Attribute')
        verbose_name_plural = _('Product Attributes')

    def __str__(self):
        # return _("Attribute: {} | Product: {}".format(self.name, self.product.title))
        return _("Id: {} | Name: {}".format(self.id, self.name))

    def to_string(self):
        return self.name
