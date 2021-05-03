from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from user_product.models import EcommerceUnsyncedProduct, UserVariant


class EcommerceUnsyncVariant(RandomIDModel):
    ecommerce_product = models.ForeignKey(to=EcommerceUnsyncedProduct, on_delete=models.SET_NULL, blank=True, null=True,
                                          related_name='ecommerce_variant_set', verbose_name=_('Shop'))
    variant_meta = JSONField(verbose_name=_('Variant Meta'))
    sku = models.CharField(max_length=100, verbose_name=_('SKU'), blank=True, null=True)
    user_variant_mapping = models.ForeignKey(to=UserVariant, on_delete=models.SET_NULL, blank=True, null=True,
                                             related_name='user_variant_mapping_set', verbose_name=_('Shop'))
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_ecommerce_unsync_variant'
        ordering = ['id']
        verbose_name = _('Ecommerce Unsync Variant')
        verbose_name_plural = _('Ecommerce Unsync Variant')
