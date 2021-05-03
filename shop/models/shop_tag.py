from django.db.models import ForeignKey, CASCADE, CharField, DateTimeField

from HUB.models.random_id_model import RandomIDModel
from shop.models.shop import Shop


class ShopTag(RandomIDModel):
    shop = ForeignKey(to=Shop, related_name='tags', on_delete=CASCADE)
    tag = CharField(max_length=255)

    create_time = DateTimeField(auto_now_add=True)
    update_time = DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop_shop_tag'
        ordering = ['id']
