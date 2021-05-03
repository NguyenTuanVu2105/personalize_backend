from rest_framework import viewsets
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from shipping.models import ShippingRate
from shipping.serializers import BriefShippingRateSerializer


class ShippingRateViewSet(viewsets.ModelViewSet, AuthenticatedGenericViewSet):
    queryset = ShippingRate.objects.all()
    serializer_class = BriefShippingRateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(self.serializer_class(queryset, many=True).data)
