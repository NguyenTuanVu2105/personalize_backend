from django.urls import path, include
from rest_framework import routers

from .views import PaypalBillingAgreementAPIView, PaypalPaymentMethodViewSet, PaypalAuthorizationAPIView
from .views.paypal_customer_view import PaypalCustomerAPIView
from .views.paypal_order_viewset import PaypalOrderViewSet
from .views.paypal_sale_webhook_view import PaypalSaleWebhookView

paypal_method_router = routers.DefaultRouter()
paypal_method_router.register(r'', PaypalPaymentMethodViewSet)


paypal_order_router = routers.DefaultRouter()
paypal_order_router.register(r'', PaypalOrderViewSet, basename='paypal_order')

paypal_method_urlpatterns = [
    path("billing-agreements", PaypalBillingAgreementAPIView.as_view()),
    path("client-id", PaypalAuthorizationAPIView.as_view()),
    path("customer", PaypalCustomerAPIView.as_view()),
    path("orders/", include(paypal_order_router.urls)),
    path("methods/", include(paypal_method_router.urls)),
    path("sale/hook", PaypalSaleWebhookView.as_view())
]

urlpatterns = [
    path("paypal/", include(paypal_method_urlpatterns))
]
