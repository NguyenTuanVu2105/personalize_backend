from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from .user_variant import UserVariant


class UserVariantPrice(RandomIDModel):
    user_variant = models.ForeignKey(UserVariant, on_delete=models.SET_NULL, blank=True, null=True, related_name='prices', verbose_name=_('User Variant'))
    currency = models.CharField(max_length=3, verbose_name=_('Currency'))
    value = models.DecimalField(max_digits=20, decimal_places=2)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_variant_price'
        unique_together = ('user_variant', 'currency')
        ordering = ['id']
