from rest_framework import serializers

from ..models import ArtworkFusionInfo


class ArtworkFusionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkFusionInfo
        fields = ('id', 'artwork', 'frame', 'layer', 'rotation', 'position', 'scale', 'is_hidden')
