from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClientTokenAPIView, PaymentMethodViewSet

payment_method_router = DefaultRouter()
payment_method_router.register(r'', PaymentMethodViewSet)

braintree_payment_urlpatterns = [
    path('token', ClientTokenAPIView.as_view()),
    path('methods/', include(payment_method_router.urls))
]

urlpatterns = [
    path('braintree/', include(braintree_payment_urlpatterns))
]
