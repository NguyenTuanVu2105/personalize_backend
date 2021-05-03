from rest_framework import serializers

from ..models import CategoryProduct


class CategoryProductSerializer(serializers.ModelSerializer):
    id = serializers.JSONField()
    title = serializers.JSONField()
    preview_image_url = serializers.JSONField()

    class Meta:
        model = CategoryProduct
        fields = ('id', 'title', 'preview_image_url')
