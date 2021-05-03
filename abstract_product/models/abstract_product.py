from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from abstract_product.constants import ABSTRACT_TYPE_CHOICES, AbstractType
from abstract_product.managers import AbstractProductManager


class AbstractProduct(RandomIDModel):
    categories = models.ManyToManyField('abstract_product.AbstractProductCategory',
                                        related_name='child_abstract_products',
                                        through='abstract_product.CategoryProduct')
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.CharField(max_length=255, null=True, verbose_name=_('Slug'))
    sku = models.CharField(max_length=255, verbose_name=_('SKU'), null=True)
    is_active = models.BooleanField()
    is_catalog_visible = models.BooleanField(default=True)
    preview_image_url = models.CharField(max_length=512, null=True, verbose_name=_('Preview Image Url'))
    sort_index = models.SmallIntegerField(default=0, verbose_name='Sort Index')
    active_mockup_version = models.CharField(max_length=4, default="v1")
    type = models.CharField(max_length=2, choices=ABSTRACT_TYPE_CHOICES, default=AbstractType.FLAT_PRODUCT)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    tsv_metadata_search = SearchVectorField(null=True)

    objects = AbstractProductManager()

    class Meta:
        db_table = 'abstract_product'
        ordering = ['sort_index', 'id']
        verbose_name = _('Abstract Product')
        verbose_name_plural = _('Abstract Products')

    def __str__(self):
        return self.title

    @property
    def combine_fusion(self):
        return self.meta.fusion_meta['fusion_combination']

    def get_colors(self):
        colors = []
        color_attribute_queryset = self.child_attributes.filter(name='Color')
        if len(color_attribute_queryset) == 0:
            colors = ['#333333']
        else:
            color_attribute = color_attribute_queryset.first()
            for color in color_attribute.child_attributes_value_set.all():
                colors.append(color.value)
        return colors
