from rest_framework.serializers import ModelSerializer

from user.models import UserTag


class UserTagSerializer(ModelSerializer):
    class Meta:
        model = UserTag
        fields = '__all__'


class UserTagWithoutUserIdSerializer(ModelSerializer):
    class Meta:
        model = UserTag
        fields = ['id', 'tag']
