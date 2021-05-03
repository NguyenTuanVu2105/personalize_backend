from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from abstract_product.models.abstract_product_variant import AbstractProductVariant


class UserAbstractVariantDefaultPrice(RandomIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_variant_default_price_set', verbose_name=_('User'))
    abstract_variant = models.ForeignKey(AbstractProductVariant, on_delete=models.CASCADE,
                                         related_name='abstract_variant_default_price_set', verbose_name=_('Abstract Variant'))
    currency = models.CharField(max_length=3, verbose_name=_('Currency'))
    price = models.DecimalField(max_digits=11, decimal_places=2)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_abstract_variant_default_price'
        ordering = ['id']
        verbose_name = _('Variant Default Price')
        verbose_name_plural = _('Variant Default Price')

    def __str__(self):
        return _("Variant Default Price: {}".format(self.id))

    def parse_info(self):
        data = {
            "id": self.id,
            "user": self.user.id,
            "abstract_variant": self.abstract_variant.id,
            "currency": self.currency,
            "price": self.price,
            "update_time": self.update_time
        }
        return data
