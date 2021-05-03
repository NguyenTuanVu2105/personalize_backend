from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from .abstract_product import AbstractProduct
from .abstract_product_variant import AbstractProductVariant


def default_pricing_meta():
    return {
        "extra_artwork": 0
    }


def default_shipping_meta():
    return {
        "shipping_time": "3 business days"
    }


def default_template_meta():
    return {
        "template_url": "",
        "mockup_samples": {}
    }


def default_fusion_meta():
    return {
        "fusion_combination": False,
    }


class AbstractProductMeta(RandomIDModel):
    abstract_product = models.OneToOneField(AbstractProduct, on_delete=models.CASCADE, unique=True, related_name='meta',
                                            null=True)
    description = models.TextField(verbose_name=_("Description"))
    short_description = models.TextField(verbose_name=_("Short Description"), default='')
    default_variant = models.ForeignKey(AbstractProductVariant, on_delete=models.SET_NULL, null=True,
                                        related_name='default_of_product')
    base_cost = models.DecimalField(max_digits=11, decimal_places=2, verbose_name=_('Base Cost'))
    pricing_meta = JSONField(default=default_pricing_meta)
    shipping_meta = JSONField(default=default_shipping_meta)

    template_meta = JSONField(default=default_template_meta)
    fusion_meta = JSONField(default=default_fusion_meta)

    design_note = models.TextField(null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'abstract_product_meta'
        ordering = ['id']
        verbose_name = _('Abstract Product Meta')
        verbose_name_plural = _('Abstract Products Meta')

    def __str__(self):
        return self.abstract_product.title
