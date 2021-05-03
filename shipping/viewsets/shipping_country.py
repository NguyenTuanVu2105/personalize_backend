from rest_framework import viewsets
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from shipping.models import ShippingCountry
from shipping.serializers import ShippingCountrySerializer


class ShippingCountryViewSet(viewsets.ModelViewSet, AuthenticatedGenericViewSet):
    queryset = ShippingCountry.objects.all().filter(is_active=True)
    serializer_class = ShippingCountrySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(self.serializer_class(queryset, many=True).data)
