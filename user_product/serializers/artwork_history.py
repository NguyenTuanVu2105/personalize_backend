from rest_framework import serializers

from ..models import ArtworkHistory


class ArtworkHistorySerializer(serializers.ModelSerializer):
    original_artwork = serializers.StringRelatedField()

    class Meta:
        model = ArtworkHistory
        fields = (
            'id', 'original_artwork', 'original_name', 'original_image_url', 'original_width', 'original_height', 'create_time')
