from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from service_communication.services.adapter_services import AdapterAppCommunicationService
from service_communication.services.adapter_services.adapter_shop_communication_service import \
    AdapterShopCommunicationService
from shop.constants.shop_location_type import ShopLocationType
from shop.models import Shop, ShopLocationChange
from shop.paginations import AdminShopPagination
from shop.serializers import ShopWithOwnerSerializer
from shop.filters import ShopOwnerFilter
from shop.services.shop_xlsx import ShopWorkbook


class ShopAdmin(SearchableListModelMixin, ListModelMixin,
                RetrieveModelMixin,
                AdminGenericViewSet, UpdateModelMixin):
    queryset = Shop.objects.prefetch_related('ecommerce', 'currency', 'location_change').ecommerce_exclude().order_by(
        "-create_time")
    serializer_class = ShopWithOwnerSerializer
    pagination_class = AdminShopPagination
    filterset_class = ShopOwnerFilter

    def get_queryset(self):
        return self.queryset

    @action(methods=["POST"], detail=False, url_path="bulk_check_location")
    def check_all_location(self, request, *args, **kwargs):
        shop_ids = request.data.get("shop_ids")
        shops = Shop.objects.filter(id__in=shop_ids)
        for shop in shops:
            AdapterShopCommunicationService.check_location(shop)
        return Response({"success": True, })

    @action(methods=["POST"], detail=False, url_path="bulk_update_location")
    def update_location(self, request, *args, **kwargs):
        shop_ids = request.data.get("shop_ids")
        shops = Shop.objects.filter(id__in=shop_ids)
        for shop in shops:
            location_changes = ShopLocationChange.objects.filter(shop=shop)
            if len(location_changes) > 0:
                location_change = location_changes.filter(type=ShopLocationType.WRONG_LOCATION).first()
                if location_change:
                    shop.location_id = location_change.new_location
                    location_change.is_resolve = True
                    location_change.save()
                    shop.save()
        return Response({"success": True, })

    @action(methods=["POST"], detail=False, url_path="bulk_add_location")
    def add_location(self, request, *args, **kwargs):
        shop_ids = request.data.get("shop_ids")
        shops = Shop.objects.filter(id__in=shop_ids)
        for shop in shops:
            location_changes = ShopLocationChange.objects.filter(shop=shop)
            if len(location_changes) > 0:
                location_change = location_changes.filter(type=ShopLocationType.NOT_HAS_LOCATION).first()
                if location_change:
                    AdapterAppCommunicationService.post_init_app(shop)
                    location_change.is_resolve = True
                    location_change.save()
        return Response({"success": True, })

    @action(methods=['get'], detail=False, url_path='export')
    def export_shop_as_xlsx(self, request):
        qs = self.filter_queryset(self.get_queryset())
        workbook = ShopWorkbook(qs)
        response = workbook.get_workbook()
        return response
