import logging

from rest_framework import serializers

from HUB.serializers.generic_relation_serializers import GenericRelationSerializer
from user_product.models import UserProduct
from .shop_user_product import ShopUserProductSerializer
from .user_product_artwork_fusion import DetailUserProductSideArtworkFusionSerializer

logger = logging.getLogger(__name__)


class GenericRelationUserProductSerializer(GenericRelationSerializer):
    class Meta(GenericRelationSerializer.Meta):
        model = UserProduct


class BaseUserProductSerializer(GenericRelationUserProductSerializer):
    class Meta(GenericRelationUserProductSerializer.Meta):
        fields = ('id', 'title', 'abstract_product', 'preview_image_url', 'can_duplicate',
                  'status', 'create_time', 'update_time')


class UserProductSerializer(BaseUserProductSerializer):
    shop_user_product_set = ShopUserProductSerializer(many=True)
    order_item_count = serializers.IntegerField(read_only=True)
    order_item_quantity = serializers.IntegerField(read_only=True)

    class Meta(BaseUserProductSerializer.Meta):
        fields = BaseUserProductSerializer.Meta.fields + (
        'user', 'order_item_count', 'order_item_quantity', 'shop_user_product_set',)


class UserProductAsyncInfoSerializer(serializers.ModelSerializer):
    shop_user_product_set = ShopUserProductSerializer(many=True)
    side_artworks = DetailUserProductSideArtworkFusionSerializer(source='artwork_set', many=True)

    class Meta:
        model = UserProduct
        fields = ('id', 'shop_user_product_set', 'side_artworks')


class BriefUserProductSerializer(serializers.ModelSerializer):
    # use in Thank you card Sample, please deal with it if you want to edit

    class Meta:
        model = UserProduct
        fields = ('id', 'title', 'preview_image_url')
