from django.urls import path, include
from rest_framework import routers

from event.viewsets import AdminEventTemplateViewSet, EventTemplateViewSet

event_router = routers.DefaultRouter()
event_router.register(r'', EventTemplateViewSet)

admin_event_router = routers.DefaultRouter()
admin_event_router.register(r'', AdminEventTemplateViewSet)


urlpatterns = [
    path('event/', include(event_router.urls)),
    path('admin/event/', include(admin_event_router.urls))
]
