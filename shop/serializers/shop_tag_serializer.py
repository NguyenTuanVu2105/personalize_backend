from rest_framework.serializers import ModelSerializer

from shop.models import ShopTag


class ShopTagSerializer(ModelSerializer):
    class Meta:
        model = ShopTag
        fields = '__all__'
