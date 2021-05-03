from rest_framework import serializers

from ..models import Artwork


class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = ('id', 'name', 'file_url', 'is_public', 'status', 'width', 'height', 'create_time', 'update_time',
                  'last_used_time', 'total_created_product', "is_default", "is_legal_accepted")


class ArtworkSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = ('width', 'height')
