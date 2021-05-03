from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericAPIView
from analytics.views.billing_statistic import BillingStatisticView
from analytics.views.dashboard import OrderStatisticView
from billing.models import Transaction
from order.models import Order


class AdminOrderDashboardView(OrderStatisticView, AdminGenericAPIView):
    @method_permission_required(get_permissions(['admin_dashboard_view', ]))
    def get(self, request):
        queryset = Order.objects.all()
        return super().response_order_statistic(request, queryset)


class AdminBillingDashboardView(BillingStatisticView, AdminGenericAPIView):
    @method_permission_required(get_permissions(['admin_dashboard_view', ]))
    def get(self, request):
        queryset = Transaction.objects.all()
        return super().response_billing_statistic(request, queryset)
