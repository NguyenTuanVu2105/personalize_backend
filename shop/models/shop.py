from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.functional import cached_property

from HUB.models.random_id_model import RandomIDModel
from HUB.settings import BASE_CURRENCY
from shop.constants.shop_status import SHOP_STATUS_CHOICES, ShopStatus
from shop.managers import ShopManager
from system_metadata.models import CurrencyExchangeRate
from .ecommerce import Ecommerce

User = get_user_model()


def default_confirm_installation_params():
    return {
        "code": "",
        "hmac": "",
        "shop": "",
        "timestamp": ""
    }


class Shop(RandomIDModel):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    ecommerce = models.ForeignKey(to=Ecommerce, on_delete=models.CASCADE)
    ecommerce_shop_id = models.BigIntegerField(null=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100, default='')
    access_token = models.TextField()
    location_id = models.BigIntegerField(null=True)
    currency = models.ForeignKey(to=CurrencyExchangeRate, on_delete=models.SET_DEFAULT, default=BASE_CURRENCY)
    last_hook_uninstall_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=SHOP_STATUS_CHOICES, max_length=2, default=ShopStatus.ACTIVE, db_index=True)
    confirm_installation_params = JSONField(default=default_confirm_installation_params)
    api_error_count = models.SmallIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    tsv_metadata_search = SearchVectorField(null=True)

    objects = ShopManager()

    user_products = models.ManyToManyField(to='user_product.UserProduct', through='user_product.ShopUserProduct',
                                           related_name="shops")

    class Meta:
        db_table = 'shop'
        ordering = ['-create_time']
        unique_together = ('owner', 'url')
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    @cached_property
    def currency_exchange_rate(self):
        try:
            return self.currency.rate
        except CurrencyExchangeRate.DoesNotExist:
            return 0.0

    @property
    def verbose_status(self):
        current_status = self.status
        for status_choice in SHOP_STATUS_CHOICES:
            short_status, verbose_status = status_choice
            if short_status == current_status:
                return verbose_status

    def reset_api_error_count(self, save=True):
        self.api_error_count = 0
        if save:
            self.save()

    def is_default_printholo_shop(self):
        return self.url is None or len(self.url) == 0 or self.location_id is None

    def __str__(self):
        return self.name

    def parse_basic_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "ecommerce": self.ecommerce.name,
            "url": self.url
        }
