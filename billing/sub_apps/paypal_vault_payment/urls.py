from django.urls import path, include

from .views.paypal_capture_webhook_view import PaypalCaptureWebhookView
from .views.paypal_vault_order_view import PaypalVaultOrderAPIView
from .views.test import PaypalVaultTestView

paypal_vault_method_urlpatterns = [
    path("order", PaypalVaultOrderAPIView.as_view()),
    path("test", PaypalVaultTestView.as_view()),
    path("capture/hook", PaypalCaptureWebhookView.as_view()),
]

urlpatterns = [
    path("paypal-vault/", include(paypal_vault_method_urlpatterns))
]
