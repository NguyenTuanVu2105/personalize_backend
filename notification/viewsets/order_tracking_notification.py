from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin

from HUB.viewsets.base import AdminGenericViewSet
from notification.constants import ORDER_TRACKING_NOTIFICATION_TYPE_CHOICES
from notification.filter import OrderTrackingNotificationFilter
from notification.models import OrderTrackingNotification
from notification.serializers import OrderTrackingNotificationSerializer


class OrderTrackingNotificationViewSet(AdminGenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                                       DestroyModelMixin, UpdateModelMixin):
    queryset = OrderTrackingNotification.objects.all().order_by('-create_time')
    serializer_class = OrderTrackingNotificationSerializer
    filterset_class = OrderTrackingNotificationFilter

    def list(self, request, *args, **kwargs):
        response = super(OrderTrackingNotificationViewSet, self).list(request, *args, **kwargs)
        if not response.data.get('options'):
            response.data['options'] = {}
        response.data['options'] = {'types': ORDER_TRACKING_NOTIFICATION_TYPE_CHOICES}
        return response
