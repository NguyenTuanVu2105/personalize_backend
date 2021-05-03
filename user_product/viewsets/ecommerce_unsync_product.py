from rest_framework import mixins
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from rest_framework.decorators import action
from django.db.models import Prefetch

from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from shop.models import Shop
from user_product.functions import create_user_product_from_ecomerce_product
from user_product.functions.create_user_mapping_variant import create_user_mapping_variant
from user_product.functions.create_variant_artwork_and_relation import create_variant_artwork_and_relation
from user_product.models import EcommerceUnsyncedProduct, EcommerceUnsyncVariant, ShopUserProduct, UserVariant
from user_product.serializers.shop_ecommerce_unsync_product import EcommerceUnsyncProductSerializer, \
    EcommerceUnsyncProductDetailSerializer
from user_product.services.ecommerce_unsync_product import get_all_product_in_store
from django.db.models import Q

import logging

logger = logging.getLogger(__name__)


class EcommerceUnsyncProductViewSet(AuthenticatedGenericViewSet, SearchableListModelMixin, mixins.RetrieveModelMixin):
    queryset = EcommerceUnsyncedProduct.objects.all().order_by('-update_time')
    serializer_class = EcommerceUnsyncProductSerializer

    def get_query_set(self):
        return self.queryset.filter(shop__owner__id=self.request.user.pk)

    def get_detail_query(self):
        return self.get_query_set().prefetch_related(
            "ecommerce_variant_set",
            "ecommerce_variant_set__user_variant_mapping"
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_query_set()
        self.queryset = queryset
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            ecommerce_product = self.get_detail_query()
            self.queryset = ecommerce_product
            self.serializer_class = EcommerceUnsyncProductDetailSerializer
            return super().retrieve(self, request, *args, **kwargs)
        except Exception as e:
            return Response("error")

    @action(methods=["POST"], detail=False, url_path="sync_from_shop")
    def sync_product(self, request):
        shop = Shop.objects.get(url=request.data["shop_url"])
        products = get_all_product_in_store(shop)
        try:
            for product in products:
                current_product = ShopUserProduct.objects.filter(product_id=product['id'], shop=shop)
                if not current_product:
                    ecomerce_product = EcommerceUnsyncedProduct.objects.create(shop=shop, product_meta=product,
                                                                               ecommerce=shop.ecommerce,
                                                                               title=product['title'],
                                                                               description=product['body_html'],
                                                                               is_active=True)
                    for variant in ecomerce_product.product_meta['variants']:
                        EcommerceUnsyncVariant.objects.create(ecommerce_product=ecomerce_product, variant_meta=variant,
                                                              sku=variant['sku'])
        except Exception as e:
            return Response({"success": False, "error": str(e)})
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="map_variant")
    def map_variant(self, request):
        request_data = request.data
        try:
            ecomerce_variant = EcommerceUnsyncVariant.objects.get(id=request_data['ecomerce_variant_id'])
            user_variant = UserVariant.objects.get(id=request_data['user_variant_id'])

            ecomerce_variant.user_variant_mapping = user_variant
            ecommerce_product = ecomerce_variant.ecommerce_product
            user_product = ecommerce_product.user_product_mapping
            user_id = request.user.id
            if user_product is None:
                create_user_product_from_ecomerce_product(ecommerce_product, user_id)
            ecomerce_variant.save()
        except Exception as e:
            return Response({"success": False, "error": str(e)})
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="create_mapping_variant")
    def create_mapping_variant(self, request):
        request_data = request.data
        try:
            ecomerce_variant = EcommerceUnsyncVariant.objects.get(id=request_data['ecomerce_variant_id'])
            abstract_variant_id = request_data['abstract_variant_id']
            user_id = request.user.id
            artworks = request_data['artworks'] if 'artworks' in request_data else []
            user_variant = create_user_mapping_variant(ecomerce_variant, abstract_variant_id, artworks, user_id)
            if 'artworks' in request_data:
                image_url = None
                if 'image' in ecomerce_variant.variant_meta:
                    image_url = ecomerce_variant.variant_meta['image']['src']
                create_variant_artwork_and_relation(user_variant, artworks, image_url, user_id)

        except Exception as e:
            return Response({"success": False, "error": str(e)})
        return Response({"success": True})
