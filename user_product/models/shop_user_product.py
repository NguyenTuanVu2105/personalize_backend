from django.db import models
from django.utils.translation import gettext as _

from HUB.models.random_id_model import RandomIDModel
from user_product.constants.shop_user_product_sync_status import SHOP_USER_PRODUCT_SYNC_STATUS_CHOICES, ShopUserProductSyncStatus
from .user_product import UserProduct


class ShopUserProduct(RandomIDModel):
    shop = models.ForeignKey('shop.Shop', on_delete=models.SET_NULL, blank=True, null=True, related_name='user_product_set', verbose_name=_('Shop'))
    user_product = models.ForeignKey(UserProduct, on_delete=models.SET_NULL, blank=True, null=True, related_name='shop_user_product_set', verbose_name=_('User Product'))
    product_id = models.CharField(max_length=20, null=True, blank=True)
    handle = models.CharField(max_length=255, null=True, blank=True)
    sync_status = models.CharField(max_length=1, choices=SHOP_USER_PRODUCT_SYNC_STATUS_CHOICES, default=ShopUserProductSyncStatus.NEW)
    sync_status_message = models.TextField(null=True, verbose_name=_('Sync Status Message'))
    is_active = models.BooleanField(default=True)
    is_refresh = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    @property
    def verbose_sync_status(self):
        current_fulfill_status = self.sync_status
        for status_choice in SHOP_USER_PRODUCT_SYNC_STATUS_CHOICES:
            short_status, verbose_status = status_choice
            if short_status == current_fulfill_status:
                return verbose_status

    @property
    def is_synced(self):
        return self.sync_status == ShopUserProductSyncStatus.SYNCED


    class Meta:
        db_table = 'shop_user_product'
        ordering = ['id']
        verbose_name = _('Shop User Product')
        verbose_name_plural = _('Shop User Product')

    def __str__(self):
        return _("Shop: {} | User Product: {}".format(self.shop, self.user_product))
