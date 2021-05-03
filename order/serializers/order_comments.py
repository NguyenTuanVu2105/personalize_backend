from rest_framework.serializers import ModelSerializer, SerializerMethodField

from order.models import OrderComments
from user.serializers.user import BriefUserSerializer


class BriefOrderCommentsSerializer(ModelSerializer):
    author = SerializerMethodField()

    def get_author(self, instance):
        return instance.author.name

    class Meta:
        model = OrderComments
        fields = ['author', 'content', 'create_time']


class OrderCommentsSerializer(ModelSerializer):
    author = BriefUserSerializer()

    class Meta:
        model = OrderComments
        fields = ("id", "order_id", "content", "author", "create_time", "update_time")
