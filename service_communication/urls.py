from django.urls import path, include
from rest_framework import routers

from .views import ShopifyBridge, WebhookJobViewSet
from .views.admin_incoming_webhook import AdminIncomingWebhookViewSet
from .views.admin_rejected_request import AdminRejectedRequestViewSet
from .views.request_log_viewsets import RequestLogViewSet
from .viewsets import ServiceAuthenticationConfigViewSet

webhook_job_router = routers.DefaultRouter()
webhook_job_router.register(r'', WebhookJobViewSet)

requeset_log_router = routers.DefaultRouter()
requeset_log_router.register(r'', RequestLogViewSet)

admin_rejected_request_router = routers.DefaultRouter()
admin_rejected_request_router.register(r'', AdminRejectedRequestViewSet)

admin_incoming_webhook_router = routers.DefaultRouter()
admin_incoming_webhook_router.register(r'', AdminIncomingWebhookViewSet)

admin_authentication_config = routers.DefaultRouter()
admin_authentication_config.register(r'', ServiceAuthenticationConfigViewSet)

urlpatterns = [
    path('bridge/spf/', ShopifyBridge.as_view()),
    path('admin/webhook/jobs/', include(webhook_job_router.urls)),
    path('admin/webhook/request-log/', include(requeset_log_router.urls)),
    path('admin/rejected_request/', include(admin_rejected_request_router.urls)),
    path('admin/incoming_webhook/', include(admin_incoming_webhook_router.urls)),
    path('admin/authentication_config/', include(admin_authentication_config.urls)),
]
