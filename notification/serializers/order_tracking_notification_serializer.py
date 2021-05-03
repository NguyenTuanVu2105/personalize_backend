from rest_framework.serializers import ModelSerializer

from notification.models import OrderTrackingNotification


class OrderTrackingNotificationSerializer(ModelSerializer):
    class Meta:
        model = OrderTrackingNotification
        fields = '__all__'
        read_only_fields = ["id", "order"]
