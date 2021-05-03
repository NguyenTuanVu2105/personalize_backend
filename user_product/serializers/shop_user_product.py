from rest_framework.fields import CharField

from HUB.serializers.generic_relation_serializers import GenericRelationSerializer
from shop.serializers.shop import ShopSerializer
from user_product.models import ShopUserProduct


class GenericRelationShopUserProductSerializer(GenericRelationSerializer):
    class Meta(GenericRelationSerializer.Meta):
        model = ShopUserProduct


class ShopUserProductSerializer(GenericRelationShopUserProductSerializer):
    shop = ShopSerializer()
    sync_status = CharField(source="verbose_sync_status")

    class Meta(GenericRelationShopUserProductSerializer.Meta):
        fields = (
            'id', 'shop', 'product_id', 'handle', 'user_product', 'is_active', 'sync_status', 'sync_status_message',
            'create_time',
            'update_time')
