import logging

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from service_communication.services.adapter_services import AdapterOrderCommunicationService
from shop.functions.update_shipping_rate_mapping import update_shipping_rate_mapping
from shop.models import ShopShippingRateMapping, Shop
from shop.serializers.shipping_rate_mapping import ShopShippingRateMappingSerializer
from shipping.models import ShippingRate
from system_metadata.serializers.shipping_rate import ShippingRateSerializer

logger = logging.getLogger(__name__)


class ShopShippingRateMappingViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ShopShippingRateMapping.objects.all()

    def get_queryset(self):
        return self.queryset.filter(shop__owner_id=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        shop_id = request.GET.get('shop_id', None)
        if shop_id is None:
            return Response({"success": False, "message": "shop_id is none"})
        try:
            mappings = self.get_queryset().filter(shop_id=shop_id)
            shipping_rates = ShippingRate.objects.all()
            return Response({
                'shipping_rate_mappings': ShopShippingRateMappingSerializer(mappings, many=True).data,
                'shipping_rates': ShippingRateSerializer(shipping_rates, many=True).data
            })
        except Exception as e:
            return Response({"success": False, "message": str(e)})

    @action(methods=["POST"], detail=False, url_path="update")
    def update_mapping(self, request, *args, **kwargs):
        request_data = request.data
        shipping_rate_mappings = request_data['shipping_rate_mappings']
        shop_id = request_data['shop_id']
        # update
        for mapping in shipping_rate_mappings:
            self.get_queryset().update_or_create(id=mapping['id'], shop_id=shop_id,
                                                 defaults={
                                                     'shipping_rate_id': mapping['shipping_rate'],
                                                 })
        return Response({"success": True})

    @action(methods=["GET"], detail=False, url_path="sync-shop")
    def sync_shop_rates(self, request, *args, **kwargs):
        shop_id = request.GET.get('shop_id', None)
        if shop_id is None:
            return Response({"success": False, "message": "shop_id is none"})
        try:
            shop = Shop.objects.get(pk=shop_id)
            get_shipping_rates_response = AdapterOrderCommunicationService.get_shipping_rates(shop)
            if get_shipping_rates_response['success']:
                shop_shipping_zones = get_shipping_rates_response['data']['shipping_zones']
                mappings = update_shipping_rate_mapping(shop, shop_shipping_zones)
                return Response({"success": True, 'shipping_rate_mappings': ShopShippingRateMappingSerializer(mappings, many=True).data})
            else:
                mappings = self.get_queryset().filter(shop=shop)
                return Response({"success": False, 'shipping_rate_mappings': ShopShippingRateMappingSerializer(mappings, many=True).data})
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e)})
