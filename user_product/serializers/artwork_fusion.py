import logging

from rest_framework import serializers

from . import ArtworkSerializer
from .layer_content_serializer import LayerContentSerializer
from ..models import ArtworkFusion

logger = logging.getLogger(__name__)


class ArtworkFusionSerializer(serializers.ModelSerializer):
    # artwork_set = ArtworkSerializer(source="artworks", many=True)
    layers = LayerContentSerializer(source="artwork_fusion_info_artwork_set", many=True, read_only=True)

    class Meta:
        model = ArtworkFusion
        fields = ('id', 'name', 'image_url', 'layers', 'create_time', 'update_time')
