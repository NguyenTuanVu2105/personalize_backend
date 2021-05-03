from django.urls import path, include
from rest_framework import routers

from billing.sub_apps.stripe_payment.views import StripeAPIKeyView
from .views import UserStripeCreateView, CheckoutView, UserStripeListView, OrderCard
from .viewsets import UserStripeViewSet

stripe_user_router = routers.DefaultRouter()
stripe_user_router.register(r'', UserStripeViewSet)

stripe_payment_urlpatterns = [
    path('create_stripe_user', UserStripeCreateView.as_view()),
    path('api_key', StripeAPIKeyView.as_view()),
    path('card', UserStripeListView.as_view()),
    path('checkout', CheckoutView.as_view()),
    path('reorder', OrderCard.as_view()),
    path('user/', include(stripe_user_router.urls)),

]

urlpatterns = [
    path('stripe/', include(stripe_payment_urlpatterns))
]
