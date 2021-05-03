from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel


class CategoryProduct(RandomIDModel):
    product = models.ForeignKey('abstract_product.AbstractProduct', on_delete=models.SET_NULL, blank=True, null=True, related_name='product_category_set', verbose_name=_('Product'))
    category = models.ForeignKey('abstract_product.AbstractProductCategory', on_delete=models.SET_NULL, blank=True, null=True, related_name='product_category_set', verbose_name=_('Category'))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'abstract_product_abstract_category'
        ordering = ['id']
        verbose_name = _('Abstract Product - Category')
        verbose_name_plural = _('Abstract Product - Category')

    def __str__(self):
        return _("Product: {} | Category: {}".format(self.product, self.category))
