from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from order.models import OrderHistory


class OrderHistorySerializer(ModelSerializer):
    verbose_type = CharField()

    class Meta:
        model = OrderHistory
        fields = ("id", "type", "verbose_type", "message", "old_obj", "new_obj", "create_time", "is_approved")
