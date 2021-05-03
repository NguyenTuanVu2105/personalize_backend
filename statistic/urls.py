from rest_framework import routers
from django.urls import path, include

from statistic.views import UserProductStatisticView
from statistic.viewsets import ProductStatisticViewSet, ShippingTimeStatisticViewSet, UserStatistic

abstract_production_statistic = routers.DefaultRouter()
abstract_production_statistic.register(r'', ProductStatisticViewSet)

shipping_time_statistic_router = routers.DefaultRouter()
shipping_time_statistic_router.register(r'', ShippingTimeStatisticViewSet)

user_statistic_router = routers.DefaultRouter()
user_statistic_router.register(r'', UserStatistic)

urlpatterns = [
    path('production/statistic/', include(abstract_production_statistic.urls)),
    path('shipping_time/statistic/', include(shipping_time_statistic_router.urls)),
    path('user-product/statistic/', UserProductStatisticView.as_view()),
    path('statistic/user/', include(user_statistic_router.urls)),
]
