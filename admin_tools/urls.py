from django.urls import path, include
from rest_framework import routers

from admin_tools.views import AdminCache, MockupMemoryReset
from admin_tools.views.test_get_client_ip import GetClientIP
from admin_tools.views.upload_image import AdminUploadImageViewSet
from admin_tools.viewsets import SystemSettingViewSet
from admin_tools.viewsets.mail_sender import CustomMailSenderViewSet
from admin_tools.viewsets.mail_setting import MailSettingViewSet

cache__urls = [
    path(r'', AdminCache.as_view()),
    path(r'<str:prefix>/', AdminCache.as_view())
]

mockup__urls = [
    path('reset/', MockupMemoryReset.as_view()),
]

admin_router = routers.DefaultRouter()
admin_router.register(r'images', AdminUploadImageViewSet)
admin_router.register(r'system-setting', SystemSettingViewSet)
admin_router.register(r'mail-setting', MailSettingViewSet)
admin_router.register(r'mail-sender', CustomMailSenderViewSet)

urlpatterns = [
    path('cache/', include(cache__urls)),
    path('mockup/', include(mockup__urls)),
    path('', include(admin_router.urls)),
    path('client-ip/', GetClientIP.as_view()),
]
