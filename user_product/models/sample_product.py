from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from user_product.constants import SampleProductStatus, SAMPLE_PRODUCT_STATUS_CHOICES
from user_product.managers import SampleProductManager
from user_product.models import UserProduct


class SampleProduct(RandomIDModel):
    original_product = models.OneToOneField(UserProduct, on_delete=models.SET_NULL,
                                            related_name='created_sample_product',
                                            verbose_name=_('Sample Product'), null=True)
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    preview_image_url = models.TextField(null=True)
    variant_list = JSONField(default=list())
    detail_data = JSONField()
    status = models.CharField(choices=SAMPLE_PRODUCT_STATUS_CHOICES, max_length=2, default=SampleProductStatus.ACTIVE,
                              db_index=True)
    is_highlight = models.BooleanField(default=False)
    tsv_metadata_search = SearchVectorField(null=True)

    last_refresh_data_time = models.DateTimeField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = SampleProductManager()

    class Meta:
        db_table = 'sample_product'
        ordering = ['id']
        verbose_name = _('Sample Product')
        verbose_name_plural = _('Sample Products')
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    def __str__(self):
        return _("Sample Product: {} ".format(self.id))

    @property
    def mockup_version(self):
        return self.original_product.mockup_version
