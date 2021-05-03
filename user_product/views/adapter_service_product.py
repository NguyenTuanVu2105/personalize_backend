import logging

from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.exceptions.FormValidationError import FormValidationError
from HUB.permissions.permissions import HeaderBaseAuthentication
from HUB.viewsets.base import GenericViewSet
from service_communication.constants.authenticated_service import AuthenticatedService
from shop.constants.shop_status import ShopStatus
from shop.models import Shop
from user_product.constants import ShopUserProductSyncStatus, UserProductStatus
from user_product.models import ShopUserProduct
from user_product.serializers import BaseUserProductSerializer
from django.db.models import Q

logger = logging.getLogger(__name__)


class ProductServiceAdapterViewSet(GenericViewSet):
    queryset = ShopUserProduct.objects.all()
    serializer_class = BaseUserProductSerializer

    permission_classes = [HeaderBaseAuthentication]
    service_name = AuthenticatedService.ECOMMERCE_ADAPTER

    error_messages = {
        "product": {
            "invalid": "The product is invalid",
        },
        "shop": {
            "invalid": "This shop is invalid",
        },
    }

    @action(methods=["DELETE"], detail=False, url_path="delete")
    def delete_product(self, request):
        request_data = request.data
        product_id = request_data["id"]
        shop_url = request_data["shop_url"]
        shop = Shop.objects.filter(url=shop_url, status=ShopStatus.ACTIVE).first()
        if not shop:
            raise FormValidationError(field="shop", code="invalid")
        shop_user_product = ShopUserProduct.objects.filter(product_id=product_id).first()
        if not shop_user_product:
            raise FormValidationError(field="product", code="invalid")
        shop_user_product.sync_status = ShopUserProductSyncStatus.DELETED
        user_product = shop_user_product.user_product
        shop_user_product.save()
        if not ShopUserProduct.objects.filter(Q(user_product=user_product) & ~Q(sync_status=ShopUserProductSyncStatus.DELETED)).exists():
            user_product.status = UserProductStatus.INACTIVE
            user_product.save()
        return Response({"success": True})
