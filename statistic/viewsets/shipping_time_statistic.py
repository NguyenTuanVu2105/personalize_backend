from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from HUB.permissions import get_permissions
from HUB.viewsets.base import AuthenticatedGenericViewSet
from service_communication.services.fulfill_services.fulfill_statistic_communication_service import \
    FulfillStatisticCommunicationService
from statistic.functions.update_from_dict import update_shipping_times
from statistic.models import ShippingTimeStatistic
from statistic.serializers.shipping_time_serializer import ShippingTimeStatisticSerializer


class ShippingTimeStatisticViewSet(ListModelMixin, AuthenticatedGenericViewSet):
    queryset = ShippingTimeStatistic.objects.order_by('point')
    serializer_class = ShippingTimeStatisticSerializer

    @action(methods=["GET"], detail=False, url_path='all')
    def get_all(self, request):
        return Response(ShippingTimeStatisticSerializer(self.queryset, many=True).data)

    @action(methods=["PUT"], detail=False, url_path='update',
            permission_classes=get_permissions(['admin_statistic_update']))
    def update_shipping_time(self, request):
        response = FulfillStatisticCommunicationService.get_shipping_statistic()
        if response['success']:
            update_shipping_times(response['data'])
            return Response({'success': True})
        return Response({'success': False})
