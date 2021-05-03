import logging

from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from HUB import settings
from HUB.permissions.permissions import HeaderBaseAuthentication
from service_communication.constants.authenticated_service import AuthenticatedService
from shop.constants.shop_status import ShopStatus
from shop.models import Shop

logger = logging.getLogger(__name__)


class ServiceShopView(ViewSet):
    permission_classes = [HeaderBaseAuthentication]
    service_name = AuthenticatedService.ECOMMERCE_ADAPTER

    @action(methods=["POST"], detail=False, url_path="uninstall")
    def uninstall(self, request):
        now = timezone.now()
        for shop in Shop.objects.filter(url=request.data["shop_url"], status=ShopStatus.ACTIVE):
            if shop.last_hook_uninstall_time is None or (
                    now - shop.last_hook_uninstall_time).total_seconds() > settings.SHOPIFY_APP_UNINSTALL_VIA_HOOK_DELAY_IN_SEC:
                shop.status = ShopStatus.INACTIVE
                shop.last_hook_uninstall_time = now
                shop.save()
            else:
                logger.info("Just Uninstalled")
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="update_shop")
    def update_shop(self, request):
        shop = Shop.objects.filter(url=request.data["shop_url"], status=ShopStatus.ACTIVE).first()
        if shop:
            shop.currency_id = request.data["currency"]
            shop.save()
            return Response({"success": True})
        else:
            return Response({"success": False})
