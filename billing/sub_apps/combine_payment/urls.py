from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GeneralMethodViewSet

router = DefaultRouter()
router.register("methods", GeneralMethodViewSet)

urlpatterns = [
    path('payment/', include(router.urls))
]
