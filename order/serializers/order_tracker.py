from rest_framework.serializers import ModelSerializer, CharField

from order.models import OrderTracker


class OrderTrackerSerializer(ModelSerializer):

    class Meta:
        model = OrderTracker
        fields = ("tracking_code",
                  "payloads", "update_time", "create_time")