from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from shop.models import Ecommerce, Shop
from user_product.models import UserProduct


class EcommerceUnsyncedProduct(RandomIDModel):
    shop = models.ForeignKey(to=Shop, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='shop_set', verbose_name=_('Shop'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    product_meta = JSONField(verbose_name=_('Product Meta'))
    ecommerce = models.ForeignKey(to=Ecommerce, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name='ecommerce_set', verbose_name=_('Ecommerce'))
    user_product_mapping = models.OneToOneField(UserProduct, on_delete=models.CASCADE, blank=True, null=True,
                                                unique=True,
                                                related_name='user_product_set', verbose_name=_('UserProduct'))

    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True, null=True)

    class Meta:
        db_table = 'user_ecommerce_unsync_product'
        ordering = ['update_time']
        verbose_name = _('Ecommerce Unsync Product')
        verbose_name_plural = _('Ecommerce Unsync Product')
