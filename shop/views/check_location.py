from rest_framework.mixins import ListModelMixin

from HUB.viewsets.base import AdminGenericViewSet
from shop.models import ShopLocationChange
from shop.serializers.shop_with_owner_serializer import ShopLocationChangeSerializer


class ShopCheckLocationViewSet(ListModelMixin, AdminGenericViewSet):
    queryset = ShopLocationChange.objects.all()
    serializer_class = ShopLocationChangeSerializer

