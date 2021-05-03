from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from abstract_product.models.abstract_product_variant import AbstractProductVariant
from .product_attribute_value import ProductAttributeValue


class AbstractProductVariantAttribute(RandomIDModel):
    variant = models.ForeignKey(AbstractProductVariant, related_name="attribute_value_set", on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'abstract_product_variant_attribute'
        ordering = ['id']
        unique_together = ('variant', 'attribute_value')
        verbose_name = _('Abstract Product Variant Attribute')
        verbose_name_plural = _('Abstract Product Variant Attribute')
        indexes = [
            models.Index(fields=['variant', 'attribute_value']),
        ]

    def __str__(self):
        return _("Variant: {} | Attribute Value: {}".format(self.variant, self.attribute_value))
