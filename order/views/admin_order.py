from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from order.filters.admin_order_filters import AdminOrderFilter
from order.functions.is_all_deliver_order import is_all_deliver_order
from order.models import Order
from order.serializers import OrderSerializer
from order.serializers.order import BriefAdminOrderSerializer, AdminOrderSerializer, \
    BriefAdminOrderWithInvoicesSerializer
from order.services.get_orders_as_xlsx import OrderWorkbook
from order.services.update_order_mfr_cost import bulk_update_order_mfr_cost
from shop.models import Shop
from shop.serializers.shop import BriefShopSerializer
from user.models import User
from user.serializers.user import BriefUserSerializer


class AdminOrderViewSet(SearchableListModelMixin,
                        mixins.RetrieveModelMixin,
                        AdminGenericViewSet):
    queryset = Order.objects.has_shop_filter()
    serializer_class = OrderSerializer
    filterset_class = AdminOrderFilter
    #filterset_fields = ('fulfill_status', 'financial_status', 'shop__owner', 'shop')

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_order_view', ]))
    def list(self, request, *args, **kwargs):
        self.serializer_class = BriefAdminOrderSerializer
        response = super().list(request, *args, **kwargs)
        response_data = response.data
        response_data['users'] = BriefUserSerializer(User.objects.filter(shop__orders__isnull=False).distinct(),
                                                     many=True).data
        response_data['shops'] = BriefShopSerializer(Shop.objects.filter(orders__isnull=False).distinct(),
                                                     many=True).data
        return response

    @method_permission_required(get_permissions(['admin_order_view', ]))
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().prefetch_related('packs',
                                                        'packs__cancel_shipping_requests',
                                                        'packs__items',
                                                        'shop',
                                                        'shop__currency',
                                                        'customer_info'
                                                        )
        order = queryset.get(id=kwargs['pk'])
        return Response(AdminOrderSerializer(order).data)

    @action(methods=["GET"], detail=False, url_path="with-invoices", permission_classes=get_permissions(['admin_billing_view']))
    def with_invoices(self, request, *args, **kwargs):
        self.serializer_class = BriefAdminOrderWithInvoicesSerializer
        response = super().list(request, *args, **kwargs)
        response_data = response.data
        response_data['users'] = BriefUserSerializer(User.objects.filter(shop__orders__isnull=False).distinct(),
                                                     many=True).data
        response_data['shops'] = BriefShopSerializer(Shop.objects.filter(orders__isnull=False).distinct(),
                                                     many=True).data
        return response

    @action(methods=['PUT', 'PATCH'], detail=False, url_path='update-all-order-mfr-cost')
    def update_order_mfr_cost_from_ffm(self, request, *args, **kwargs):
        return Response(bulk_update_order_mfr_cost())

    @action(methods=['GET'], detail=False, url_path='exports')
    def export_orders_as_xlsx(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        workbook = OrderWorkbook(queryset)
        response = workbook.get_workbook()
        return response

    @action(methods=['POST'], detail=True, url_path='update_deliver')
    def update_deliver(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        order.deliver = is_all_deliver_order(order)
        order.save()
        return Response({"success": True})