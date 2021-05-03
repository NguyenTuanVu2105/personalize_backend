from HUB.viewsets.base import BaseGenericAPIView
from analytics.views.billing_statistic import BillingStatisticView
from analytics.views.order_statistic import OrderStatisticView
from billing.models import Transaction
from order.models import Order


class DashboardView(OrderStatisticView, BaseGenericAPIView):
    def get(self, request):
        queryset = Order.objects.filter_by_user_id(self.request.user.pk)
        return super().response_order_statistic(request=request, queryset=queryset)


class BillingDashboardView(BillingStatisticView, BaseGenericAPIView):
    def get(self, request):
        queryset = Transaction.objects.filter_by_user(self.request.user.pk)
        return super().response_billing_statistic(request, queryset)
