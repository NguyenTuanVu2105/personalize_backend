from rest_framework.fields import CharField

from user.serializers.user import BriefUserSerializer
from .shop_tag_serializer import ShopTagSerializer
from .shop import ShopSerializer
from rest_framework.serializers import FloatField, IntegerField, ModelSerializer
from shop.models import Shop, ShopLocationChange

class ShopLocationChangeSerializer(ModelSerializer):
    class Meta:
        model = ShopLocationChange
        fields = ['shop_id', 'shopify_response', 'new_location', 'old_location', 'is_resolve', 'create_time', 'update_time', 'type']


class ShopWithOwnerSerializer(ShopSerializer):
    currency_exchange_rate = FloatField(source='currency.rate')
    currency_precision = IntegerField(source='currency.precision')
    owner = BriefUserSerializer()
    location_change = ShopLocationChangeSerializer(many=True)
    updatable_status = CharField(source='status')

    tags = ShopTagSerializer(many=True)

    class Meta:
        model = Shop
        fields = ['ecommerce', 'tags', 'owner', 'id', 'name', 'currency', 'url', 'currency_exchange_rate', 'currency_precision',
                  'update_time', 'status', 'location_change', 'location_id', 'updatable_status']


