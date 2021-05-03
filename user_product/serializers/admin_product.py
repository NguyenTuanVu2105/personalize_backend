import logging

from django.db.models import Count, Sum
from rest_framework import serializers

from HUB.serializers.generic_relation_serializers import GenericRelationSerializer
from abstract_product.serializers.brief_abstract_product import BriefAbstractProductSerializer
from user.serializers.user import BriefUserSerializer
from user_product.models import UserProduct
from .shop_user_product import ShopUserProductSerializer
from .user_product_artwork_fusion import DetailUserProductSideArtworkFusionSerializer

logger = logging.getLogger(__name__)


class GenericRelationAdminProductSerializer(GenericRelationSerializer):
    class Meta(GenericRelationSerializer.Meta):
        model = UserProduct


class BaseAdminProductSerializer(GenericRelationAdminProductSerializer):
    class Meta(GenericRelationAdminProductSerializer.Meta):
        fields = ('id', 'title', 'abstract_product', 'preview_image_url',
                  'status', 'create_time', 'update_time')


class AdminProductSerializer(BaseAdminProductSerializer):
    shop_user_product_set = ShopUserProductSerializer(many=True)
    order_item_count = serializers.IntegerField(read_only=True)
    order_item_quantity = serializers.IntegerField(read_only=True)
    created_sample_product = serializers.PrimaryKeyRelatedField(read_only=True)
    artwork_fusions = serializers.SerializerMethodField()
    is_valid_sample_creating = serializers.SerializerMethodField()
    user = BriefUserSerializer()

    def get_artwork_fusions(self, product):
        artwork_fusions = []
        artwork_set = product.artwork_set.all()
        for artwork in artwork_set:
            if artwork.send_to_fulfill:
                artwork_fusions.append(artwork.artwork_fusion.image_url)
        return artwork_fusions

    def get_is_valid_sample_creating(self, product):
        side_length = len(product.abstract_product.sides.all())
        artwork_fusions = []
        artwork_set = product.artwork_set.all()
        for artwork in artwork_set:
            if artwork.send_to_fulfill and artwork.artwork_fusion.image_url:
                artwork_fusions.append(artwork.artwork_fusion.image_url)

        if product.combine_fusion:
            return len(artwork_fusions) >= 1
        else:
            return len(artwork_fusions) == side_length

    class Meta(BaseAdminProductSerializer.Meta):
        fields = BaseAdminProductSerializer.Meta.fields + (
            'user', 'order_item_count', 'order_item_quantity', 'shop_user_product_set', 'created_sample_product',
            'artwork_fusions', 'is_valid_sample_creating', 'is_updated_fusions', 'background_color', 'combine_fusion')


class AdminUserProductDetailSerializer(serializers.ModelSerializer):
    shop_user_product_set = ShopUserProductSerializer(many=True)
    side_artworks = DetailUserProductSideArtworkFusionSerializer(source='artwork_set', many=True)
    abstract_product = BriefAbstractProductSerializer()
    order_item_count = serializers.SerializerMethodField()
    mockups = serializers.SerializerMethodField()
    variants = serializers.SerializerMethodField()
    child_attributes_data = serializers.SerializerMethodField()
    user = BriefUserSerializer()

    def get_order_item_count(self, object):
        return object.user_product_variant_set.all().aggregate(order_items__quantity=Sum('order_items__quantity'),
                                                               order_items__count=Count('order_items'))

    def get_variants(self, instance):
        from .user_product_detail import AdminUserVariantSerializerPrice
        return [AdminUserVariantSerializerPrice(variant).data for variant in instance.user_product_variant_set.all()]

    def get_child_attributes_data(self, instance):
        from .user_product_detail import ProductAttributeSerializer
        return [ProductAttributeSerializer(attr).data for attr in instance.abstract_product.child_attributes.all()]

    def get_mockups(self, product):
        mockups = []
        for user_variant in product.user_product_variant_set.all():
            for mockup in user_variant.mockup_per_side.all():
                if mockup.mockup_url not in mockups:
                    mockups.append(mockup.mockup_url)

        return mockups

    class Meta:
        model = UserProduct
        fields = (
            'id', 'user', 'order_item_count', 'shop_user_product_set', 'title', 'description', 'abstract_product',
            'preview_image_url', 'create_time', 'status', 'update_time', 'side_artworks', 'mockups', 'background_color',
            'is_updated_fusions', 'combine_fusion', 'variants', 'child_attributes_data')
