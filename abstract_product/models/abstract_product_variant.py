from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from .abstract_product import AbstractProduct
from .abstract_product_mockup_info import AbstractProductMockupInfo
from .product_attribute_value import ProductAttributeValue
from ..constants.attribute_type import AttributeType

DEFAULT_COLOR = "#333333"


class AbstractProductVariant(RandomIDModel):
    product = models.ForeignKey(AbstractProduct, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='abstract_product_variants', verbose_name=_('Product'))
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    sku = models.CharField(max_length=100, verbose_name=_('SKU'))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    attributes_value = models.ManyToManyField(ProductAttributeValue, related_name='variant_set',
                                              through='abstract_product.AbstractProductVariantAttribute')
    mockup_info = models.ForeignKey(AbstractProductMockupInfo, on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='variants', verbose_name=_('Mockup Info'))

    class Meta:
        db_table = 'abstract_product_variant'
        # unique_together = ('product', 'title', 'sku')
        ordering = ['id']
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')

    def __str__(self):
        return _("Variant: {} | Product: {}".format(self.id, self.product))

    @property
    def description(self):
        return " / ".join(list(map(lambda attr_value: attr_value.label, self.attributes_value.all())))

    def get_color_value(self):
        for attribute_value in self.attribute_value_set.all():
            if attribute_value.attribute_value.attribute.type == AttributeType.COLOR:
                return attribute_value.attribute_value.value
        return DEFAULT_COLOR
