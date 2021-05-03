from django.urls import path, include
from rest_framework import routers

from .viewsets import ShippingCountryViewSet, ShippingRateViewSet

seller_router = routers.DefaultRouter()
seller_router.register(r'shipping-country', ShippingCountryViewSet)
seller_router.register(r'shipping-plan', ShippingRateViewSet)

urlpatterns = [
    path('seller/', include(seller_router.urls)),
]
