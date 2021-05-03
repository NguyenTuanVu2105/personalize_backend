from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import IsAuthenticated
from HUB.viewsets.base import AdminGenericViewSet
from system_metadata.constants import DEFAULT_CURRENCY
from system_metadata.models import CurrencyExchangeRate
from system_metadata.serializers import CurrencyExchangeRateSerializer


class CurrencyExchangeRateViewSet(AdminGenericViewSet):
    serializer_class = CurrencyExchangeRateSerializer
    queryset = CurrencyExchangeRate.objects.all()

    @action(methods=["GET"], detail=False, url_path="default", permission_classes=[IsAuthenticated, ])
    def retrieve_default_currency(self, request, *args, **kwargs):
        default_currency = CurrencyExchangeRate.objects.get(pk=DEFAULT_CURRENCY)
        return Response(self.get_serializer(default_currency).data)
