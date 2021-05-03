from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from order.filters.order_invalid_filter import OrderInvalidFilter
from order.models.order_invallid import OrderInvalid
from order.serializers.order_invalid import OrderInvalidSerializer
from shop.models import Shop


class InvalidOrderViewSet(SearchableListModelMixin,
                          AdminGenericViewSet):
    queryset = OrderInvalid.objects.all()
    serializer_class = OrderInvalidSerializer
    filterset_class = OrderInvalidFilter

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_order_invalid_view']))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=["GET"], detail=False, url_path="shop")
    def get_all_shop_url(self, request, *arg, **kwargs):
        shop_list = self.get_queryset().order_by("shop__id").values_list('shop__id', flat=True).distinct()
        return Response([shop.url for shop in Shop.objects.filter(id__in=shop_list)])