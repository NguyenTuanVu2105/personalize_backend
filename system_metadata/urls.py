from django.urls import path, include
from rest_framework import routers

from system_metadata.views.admin_policy import AdminPolicyViewSet
from system_metadata.views.currency_exchange_rate import CurrencyExchangeRateViewSet
from system_metadata.views.health_check import HealthCheckViewSet
from system_metadata.views.policy import PolicyViewSet
from system_metadata.views.shipping_rate import ShippingRateViewSet

health_check_router = routers.DefaultRouter()
health_check_router.register(r'', HealthCheckViewSet, base_name='health_check')

currency_exchange_rate_router = routers.DefaultRouter()
currency_exchange_rate_router.register(r'', CurrencyExchangeRateViewSet)

shipping_rate_router = routers.DefaultRouter()
shipping_rate_router.register(r'', ShippingRateViewSet)

policy_router = routers.DefaultRouter()
policy_router.register(r'policy', PolicyViewSet)

admin_policy_router = routers.DefaultRouter()
admin_policy_router.register(r'policy', AdminPolicyViewSet)

urlpatterns = [
    path('health_check/', include(health_check_router.urls)),
    path('currency/', include(currency_exchange_rate_router.urls)),
    path('shipping_rate/', include(shipping_rate_router.urls)),
    path('user/', include(policy_router.urls)),
    path('admin/', include(admin_policy_router.urls)),
]
