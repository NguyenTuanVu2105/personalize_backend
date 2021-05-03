from rest_framework import serializers

from user_product.models import UserProduct


class UserProductWithPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProduct
        fields = ('id', 'preview_image_url')
