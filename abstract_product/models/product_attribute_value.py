from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from .product_attribute import ProductAttribute


class ProductAttributeValue(RandomIDModel):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.SET_NULL, blank=True, null=True, related_name='child_attributes_value_set', verbose_name=_('Product Attribute Name'))
    label = models.CharField(max_length=100, verbose_name=_('Product Attribute Label'))
    value = models.CharField(max_length=100, verbose_name=_('Product Attribute Value'))
    sort_index = models.SmallIntegerField(verbose_name=_('Sort Index'), default=0)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'abstract_product_attribute_value'
        ordering = ['attribute__sort_index', 'attribute__name']
        verbose_name = _('Product Attribute Value')
        verbose_name_plural = _('Product Attribute Values')

    def __str__(self):
        return _("Attribute Value: {} | Attribute: {}".format(self.label, self.attribute.name))
