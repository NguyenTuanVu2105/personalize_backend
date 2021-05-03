from django.urls import path, include

from analytics.views import DashboardView, BestSellingVariantView, BillingDashboardView
from analytics.views.admin_dashboard import AdminOrderDashboardView, AdminBillingDashboardView

analytic_url_patterns = [
    path('orders/', DashboardView.as_view()),
    path('billings/', BillingDashboardView.as_view()),
    path('best_selling_products/', BestSellingVariantView.as_view()),
    path('admin/orders/', AdminOrderDashboardView.as_view()),
    path('admin/billings/', AdminBillingDashboardView.as_view()),
]

urlpatterns = [
    path('analytics/', include(analytic_url_patterns)),
]
