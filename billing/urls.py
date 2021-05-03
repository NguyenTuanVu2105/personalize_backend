from django.urls import path, include
from rest_framework.routers import DefaultRouter

from billing.views.admin_transaction import AdminTransactionViewSet
from billing.views.refund import AdminRefundViewSet
from .views import InvoiceViewSet, TransactionViewSet
from .views.admin_invoice import AdminInvoiceViewSet

router = DefaultRouter()
router.register('invoices', InvoiceViewSet)
router.register('transactions', TransactionViewSet)
router.register('admin/refund', AdminRefundViewSet)
router.register('admin/transactions', AdminTransactionViewSet)
router.register('admin/invoices', AdminInvoiceViewSet)

urlpatterns = [
    path('billing/', include(router.urls)),
    path('hook/payments', include(router.urls)),
]
