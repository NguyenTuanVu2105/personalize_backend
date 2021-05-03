import os
from datetime import datetime

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from abstract_product.models import AbstractProduct
from user_product.constants.user_product_status import USER_PRODUCT_STATUS_CHOICES, UserProductStatus
from user_product.managers import UserProductManager


class UserProduct(RandomIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='product_set', verbose_name=_('User'))
    abstract_product = models.ForeignKey(to=AbstractProduct, on_delete=models.SET_NULL, blank=True, null=True,
                                         related_name='user_product_set', verbose_name=_('Abstract Product'))
    preview_image_url = models.TextField(null=True)
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)
    shop = models.ManyToManyField('shop.Shop', related_name='user_products_set', through='user_product.ShopUserProduct')
    status = models.CharField(choices=USER_PRODUCT_STATUS_CHOICES, max_length=2, default=UserProductStatus.ACTIVE,
                              db_index=True)
    extra_cost = models.DecimalField(max_digits=11, decimal_places=2, verbose_name=_('Extra Cost'), default=0)
    sample_product = models.ForeignKey('user_product.SampleProduct', on_delete=models.SET_NULL, blank=True, null=True,
                                       related_name='created_user_products', verbose_name=_('Original Sample Product'))

    background_color = models.CharField(max_length=8, null=True)
    is_updated_fusions = models.BooleanField(default=False)
    mockup_version = models.CharField(max_length=4, default="v1")

    tsv_metadata_search = SearchVectorField(null=True)

    objects = UserProductManager()

    class Meta:
        db_table = 'user_product'
        ordering = ['id']
        unique_together = ('user', 'sample_product')
        verbose_name = _('User Product')
        verbose_name_plural = _('User Product')
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    def __str__(self):
        return _("User Product: {}".format(self.id))

    @property
    def combine_fusion(self):
        return self.abstract_product.meta.fusion_meta['fusion_combination']

    @property
    def combine_fusion_meta(self):
        return self.abstract_product.meta.fusion_meta

    @property
    def additional_fusion_sides(self):
        fusion_meta = self.combine_fusion_meta
        if 'additional_fusion_sides' in fusion_meta:
            return fusion_meta['additional_fusion_sides']
        else:
            return None

    @property
    def is_valid_fusion_amount(self):
        if self.combine_fusion:
            user_product_artwork_fusions = self.artwork_set.send_to_fulfill_filter()
            user_product_artwork_fusion = user_product_artwork_fusions.first()
            artwork_fusion = user_product_artwork_fusion.artwork_fusion
            return bool(len(user_product_artwork_fusions) == 1 and artwork_fusion.original_image_path)
        else:
            side_amount = len(self.abstract_product.sides.all())
            fusion_amount = 0
            for user_product_artwork_fusion in self.artwork_set.all():
                if user_product_artwork_fusion.artwork_fusion.original_image_path:
                    fusion_amount = fusion_amount + 1
            return side_amount == fusion_amount

    def parse_data_for_artwork_pushing(self):
        side_artworks_data = []
        for side in self.artwork_set.all():
            side_artworks_data.append(side.parse_data_for_artwork_pushing())
        return side_artworks_data

    @property
    def can_duplicate(self):
        import pytz
        utc = pytz.UTC
        support_duplicate_start_time = os.environ.get("SUPPORT_DUPLICATE_PRODUCT_TIME", "")
        support_duplicate_time = datetime.strptime(support_duplicate_start_time, '%H:%M:%S;%d/%m/%y')
        return support_duplicate_start_time and self.create_time.replace(tzinfo=utc) >= support_duplicate_time.replace(
            tzinfo=utc)

    @property
    def type(self):
        return self.abstract_product.type

    def set_status(self, status, commit=True):
        self.status = status
        if commit:
            self.save()

    ATTRIBUTE_LABELS = [('user', 'User'),
                        ('abstract_product', 'Abstract Product'),
                        ('preview_image_url', 'Product Preview Image Url'),
                        ('title', 'Product Title'),
                        ('description', 'Product Description'),
                        ('shop', 'Shop'),
                        ('status', 'Activation Status')]
