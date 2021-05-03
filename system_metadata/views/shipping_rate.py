from rest_framework import permissions, mixins

from HUB.viewsets.base import GenericViewSet
from shipping.models.shipping_rate import ShippingRate
from system_metadata.serializers.shipping_rate import ShippingRateSerializer


class ShippingRateViewSet(mixins.ListModelMixin,
                          GenericViewSet):
    authentication_classes = []
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ShippingRateSerializer
    queryset = ShippingRate.objects.all()
