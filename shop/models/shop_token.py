from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models

from HUB.models.random_id_model import RandomIDModel

User = get_user_model()


def default_shopify_response():
    return {
        "access_token": "",
        "scope": ""
    }


class ShopToken(RandomIDModel):
    shop_url = models.CharField(max_length=100, default='')
    code = models.TextField(unique=True)
    shopify_response = JSONField(default=default_shopify_response)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop_token'
        ordering = ['-create_time']

    def __str__(self):
        return "Shop Token: ".format(self.shop_url)
