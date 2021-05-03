from django_filters import IsoDateTimeFilter

from HUB.filters import BaseCreatedTimeFilter
from notification.models import OrderTrackingNotification


class OrderTrackingNotificationFilter(BaseCreatedTimeFilter):
    sent_time_since = IsoDateTimeFilter(field_name="sent_time", lookup_expr='gte')
    sent_time_until = IsoDateTimeFilter(field_name="sent_time", lookup_expr='lte')

    class Meta(BaseCreatedTimeFilter.Meta):
        model = OrderTrackingNotification
        fields = BaseCreatedTimeFilter.Meta.fields + ('sent_time_since', 'sent_time_until', 'type', )
