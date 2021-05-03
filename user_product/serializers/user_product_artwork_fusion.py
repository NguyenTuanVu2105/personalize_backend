from rest_framework import serializers

from HUB.serializers.generic_relation_serializers import GenericRelationSerializer
from abstract_product.serializers.abstract_product_side import AbstractProductSideSerializer
from user_product.models import UserProductArtworkFusion
from user_product.serializers.artwork_fusion import ArtworkFusionSerializer


class GenericRelationUserProductArtworkSerializer(GenericRelationSerializer):
    class Meta(GenericRelationSerializer.Meta):
        model = UserProductArtworkFusion


class DetailUserProductSideArtworkFusionSerializer(GenericRelationUserProductArtworkSerializer):
    side = AbstractProductSideSerializer(source='product_side')
    fused_artwork = ArtworkFusionSerializer(source="artwork_fusion")

    class Meta(GenericRelationUserProductArtworkSerializer.Meta):
        fields = ('side', 'fused_artwork', 'send_to_fulfill')
