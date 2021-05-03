from django.urls import path, include
from rest_framework import routers

from coupon.views.admin import AdminCouponViewSet, AdminCouponCampaignViewSet, AdminRedeemedCouponTransactionViewSet
from coupon.views.user import UserCouponViewSet

user_coupon_router = routers.DefaultRouter()
user_coupon_router.register(r'coupons', UserCouponViewSet)


admin_coupon_router = routers.DefaultRouter()
admin_coupon_router.register(r'coupon-campaigns', AdminCouponCampaignViewSet)
admin_coupon_router.register(r'coupons', AdminCouponViewSet)
admin_coupon_router.register(r'coupon-transaction', AdminRedeemedCouponTransactionViewSet)

urlpatterns = [
    path('', include(user_coupon_router.urls)),
    path('admin/', include(admin_coupon_router.urls)),
]
