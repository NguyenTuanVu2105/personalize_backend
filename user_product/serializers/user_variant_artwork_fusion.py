from rest_framework import serializers

from HUB.serializers.generic_relation_serializers import GenericRelationSerializer
from user_product.models import  UserVariantArtworkFusion
from user_product.serializers.artwork_fusion import ArtworkFusionSerializer


class GenericRelationUserVariantArtworkSerializer(GenericRelationSerializer):
    class Meta(GenericRelationSerializer.Meta):
        model = UserVariantArtworkFusion


class DetailUserVariantSideArtworkFusionSerializer(GenericRelationUserVariantArtworkSerializer):
    side = serializers.CharField(source='variant_side.type')
    fused_artwork = ArtworkFusionSerializer(source="artwork_fusion")

    class Meta(GenericRelationUserVariantArtworkSerializer.Meta):
        fields = ('side', 'fused_artwork')
