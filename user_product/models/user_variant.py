from django.db import models
from django.utils.translation import gettext as _
import logging
from HUB.models.random_id_model import RandomIDModel
from abstract_product.models.abstract_product_variant import AbstractProductVariant
from user_product.managers import UserVariantManager
from .user_product import UserProduct

logger = logging.getLogger(__name__)


class UserVariant(RandomIDModel):
    user_product = models.ForeignKey(UserProduct, on_delete=models.SET_DEFAULT, related_name='user_product_variant_set',
                                     verbose_name=_('User Product'), default=0)
    abstract_variant = models.ForeignKey(AbstractProductVariant, on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='user_product_variant_set', verbose_name=_('Abstract Variant'))
    sku = models.CharField(max_length=100, verbose_name=_('SKU'), blank=True, null=True)
    sort_index = models.SmallIntegerField(verbose_name=_('Sort Index'), default=0)
    is_active = models.BooleanField(default=True)
    sample_product_variant_sku = models.CharField(max_length=16, blank=True, null=True,
                                                 verbose_name=_('Sample Product Variant SKU'))

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = UserVariantManager()

    class Meta:
        db_table = 'user_variant'
        ordering = ['update_time', 'create_time']
        unique_together = ('user_product', 'abstract_variant')
        verbose_name = _('User Variant')
        verbose_name_plural = _('User Variant')

    def __str__(self):
        return _("User Product: {} | Abstract Variant: {}".format(self.user_product, self.abstract_variant))

    @property
    def product_title(self):
        return self.user_product.title

    @property
    def type(self):
        return self.user_product.type

    def get_preview_mockup(self):
        # src = None
        # for image in self.mockup_per_side.all():
        #     if image.product_side.type == "Front" or image.product_side.type == "front":
        #         src = image.mockup_url
        # if src is None:
        #     src = self.mockup_per_side.all().first().mockup_url
        # return src
        return self.mockup_per_side.all().first().mockup_url

    ATTRIBUTE_LABELS = [('user_product', 'User Product'),
                        ('abstract_variant', 'Abstract Variant'),
                        ('sku', 'SKU'),
                        ('base_cost', 'Base Cost'),
                        ('sort_index', 'Sort Index'),
                        ('is_active', 'Activation Status')]
