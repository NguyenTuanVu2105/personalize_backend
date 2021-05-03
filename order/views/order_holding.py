from rest_framework.decorators import action

from HUB.filters import BaseCreatedTimeFilter
from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from order.models.order_holding import OrderHolding
from order.serializers.order_holding import OrderHoldingSerializer
from order.services.order_holding_xlsx import OrderHoldingWorkbook


class OrderHoldingViewSet(SearchableListModelMixin,
                          AdminGenericViewSet):
    queryset = OrderHolding.objects.all()
    serializer_class = OrderHoldingSerializer
    filterset_class = BaseCreatedTimeFilter

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_order_holding_view']))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='export')
    def export_as_xlsx(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        workbook = OrderHoldingWorkbook(queryset)
        response = workbook.get_workbook()
        return response
