from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import GenericViewSet
from rest_framework.permissions import AllowAny
from abstract_product.models.abstract_product import AbstractProduct
from user_product.models.shop_user_product import ShopUserProduct 
from abstract_product.serializers.brief_abstract_product import BriefAbstractProductSerializer
from abstract_product.functions import retrieve_abstract_product

import logging
logger = logging.getLogger(__name__)

class BuyerAbstractProductViewSet(GenericViewSet):
    queryset = AbstractProduct.objects.filter(is_active=True)
    serializer_class = BriefAbstractProductSerializer
    permission_classes = [AllowAny, ]

    @action(methods=['GET'], detail=False, url_path=r'get-abstract-by-product-id')
    def get_tracker(self, request, *args, **kwargs):
        query_params = request.query_params
        shop_url = query_params.get("shop_url")
        product_id = query_params.get("product_id")
        try:
            shop_user_product = ShopUserProduct.objects.filter(shop__url=shop_url, product_id=product_id).first()
            sku = shop_user_product.user_product.abstract_product.sku
            abstract_product = self.queryset.filter(sku=sku).first()
            return Response(retrieve_abstract_product(abstract_product.id, self.get_queryset()))
        except Exception as e:
            logger.error(e)
            return Response({"success": False})