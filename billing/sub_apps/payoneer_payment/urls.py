from django.urls import path, include
from rest_framework.routers import DefaultRouter

from billing.sub_apps.payoneer_payment.views.payoneer_payment_method import PayoneerPaymentMethodViewSet

payment_method_router = DefaultRouter()
payment_method_router.register(r'', PayoneerPaymentMethodViewSet)

payoneer_payment_urlpatterns = [
    path('methods/', include(payment_method_router.urls))
]

urlpatterns = [
    path('payoneer/', include(payoneer_payment_urlpatterns))
]
