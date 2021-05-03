from rest_framework import serializers

from ..models import AbstractProductCategory


class BriefAbstractProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractProductCategory
        fields = ('id', 'title', 'force_active', 'preview_image_url', 'sort_index', 'is_active', 'update_time')
