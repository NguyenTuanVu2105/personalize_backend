from django.urls import path, include
from rest_framework import routers

from shop.views.service_shop import ServiceShopView
from shop.views.shipping_rate_mapping import ShopShippingRateMappingViewSet
from .views import ShopViewSet, ShopAdmin, ShopCheckLocationViewSet, AdminShopTagViewSet

shop_router = routers.DefaultRouter()
shop_router.register(r'', ShopViewSet)

shop_tag_router = routers.DefaultRouter()
shop_tag_router.register(r'', AdminShopTagViewSet)

admin_shop_router = routers.DefaultRouter()
admin_shop_router.register(r'', ShopAdmin)
admin_shop_router.register(r'location', ShopCheckLocationViewSet)

shop_shipping_rate_mapping_router = routers.DefaultRouter()
shop_shipping_rate_mapping_router.register(r'', ShopShippingRateMappingViewSet,
                                           base_name='ShopShippingRateMappingViewSet')

adapter_shop_router = routers.DefaultRouter()
adapter_shop_router.register(r'', ServiceShopView, base_name='service_shop')

urlpatterns = [
    path('admin/shops/', include(admin_shop_router.urls)),
    path('shops/', include(shop_router.urls)),
    path('adapter-shop/', include(adapter_shop_router.urls)),
    path('shop-shipping-rate-mapping/', include(shop_shipping_rate_mapping_router.urls)),
    path('admin/shop-tags/', include(shop_tag_router.urls)),
]
