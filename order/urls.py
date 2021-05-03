from django.urls import path, include
from rest_framework import routers

from order.views.admin_order import AdminOrderViewSet
from order.views.service_order_pack import ServiceOrderPackViewSet
from .views import UserOrderViewSet, OrderCancelShippingRequestViewSet
from .views.adapter_service_order import OrderServiceAdapterViewSet
from .views.fulfill_service_order import OrderFulfillServiceViewSet
from .views.invalid_order import InvalidOrderViewSet
from .views.order_holding import OrderHoldingViewSet
from .views.order_tracker import OrderTrackerViewSet
from .views.tracking_tool_service_order import TrackingToolServiceView
from .viewsets.fulfillment_order_pack_view_set import AdminFulfillmentOrderPackViewSet
from .viewsets.order_comments_view_set import OrderCommentsViewSet
from .viewsets.sample_shipping_address_view_set import UserShippingAddressViewSet

user_order_router = routers.DefaultRouter()
user_order_router.register(r'', UserOrderViewSet)

sample_shipping_address_router = routers.DefaultRouter()
sample_shipping_address_router.register(r'', UserShippingAddressViewSet)

admin_order_router = routers.DefaultRouter()
admin_order_router.register(r'', AdminOrderViewSet)

order_adapter_service_router = routers.DefaultRouter()
order_adapter_service_router.register(r'', OrderServiceAdapterViewSet)

service_order_pack_router = routers.DefaultRouter()
service_order_pack_router.register(r'', ServiceOrderPackViewSet, base_name='service_order_pack')

cancel_shipping_request = routers.DefaultRouter()
cancel_shipping_request.register(r'', OrderCancelShippingRequestViewSet)

order_invalid_router = routers.DefaultRouter()
order_invalid_router.register(r'', InvalidOrderViewSet)

order_holding_router = routers.DefaultRouter()
order_holding_router.register(r'', OrderHoldingViewSet)

order_comment_router = routers.DefaultRouter()
order_comment_router.register(r'', OrderCommentsViewSet)

fulfillment_pack_router = routers.DefaultRouter()
fulfillment_pack_router.register(r'', AdminFulfillmentOrderPackViewSet)

order_tracker_router = routers.DefaultRouter()
order_tracker_router.register(r'', OrderTrackerViewSet)

urlpatterns = [
    path('orders/', include(user_order_router.urls)),
    path('admin/orders/', include(admin_order_router.urls)),
    path('hook/orders/', include(order_adapter_service_router.urls)),
    path('hook/order_packs/', include(service_order_pack_router.urls)),
    path('cancel_shipping_request/', include(cancel_shipping_request.urls)),
    path('admin/order_invalid/', include(order_invalid_router.urls)),
    path('admin/order_holding/', include(order_holding_router.urls)),
    path('sample-address/', include(sample_shipping_address_router.urls)),
    path('admin/order_comment/', include(order_comment_router.urls)),
    path('fulfillment-pack/', include(fulfillment_pack_router.urls)),
    path('order-tracker/', include(order_tracker_router.urls))
]

order_fulfill_service_router = routers.DefaultRouter()
order_fulfill_service_router.register(r'order', OrderFulfillServiceViewSet)
tracking_webhook_router = routers.DefaultRouter()
tracking_webhook_router.register(r'tracking', TrackingToolServiceView)

fulfill_service_hook_urlpatterns = [
    path('fulfill/hook/', include(order_fulfill_service_router.urls)),
    path('tracking-tool/hook/', include(tracking_webhook_router.urls))
]