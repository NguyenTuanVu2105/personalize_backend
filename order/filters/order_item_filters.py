from HUB.filters import BaseCreatedTimeFilter
from order.models import OrderItem


class OrderItemFilter(BaseCreatedTimeFilter):
    class Meta(BaseCreatedTimeFilter.Meta):
        model = OrderItem
        fields = BaseCreatedTimeFilter.Meta.fields
