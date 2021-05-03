import logging
import traceback

import django_filters
from django.db import transaction, connection
from django.db.models import Prefetch, Sum, Count
from rest_framework import filters, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.helpers.error_messages import to_standard_error_messages
from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from abstract_product.constants.abstract_type import PRODUCT_DESTROYABLE_TYPE
from abstract_product.functions import retrieve_abstract_product
from abstract_product.models import AbstractProduct, ProductAttributeValue, AbstractProductVariant, ProductAttribute
from abstract_product.serializers import ProductSerializer
from shop.models import Shop
from system_metadata.models import CurrencyExchangeRate
from user.tasks import bulk_resync_product_task
from user_product.constants import ShopUserProductSyncStatus
from user_product.constants.user_product_status import UserProductStatus
from user_product.functions import create_product_in_shop_task, retrieve_user_product_variant_with_pricing
from user_product.functions.sync_product_in_shop import update_user_product_in_all_shop_task, sync_product_in_shop_task
from user_product.functions.sync_product_in_shop.create_product import create_product_in_shop
from user_product.models import UserVariant, ShopUserProduct, UserVariantPrice, UserVariantSideMockup, \
    UserProductArtworkFusion
from user_product.serializers import UserProductAsyncInfoSerializer
from user_product.serializers.user_product_detail import UserProductDetailSerializer, BriefUserProductSerializer, \
    UserProductWithVariantsSerializer
from ..filters import UserProductFilter
from ..forms.user_product_update import UserProductUpdateForm, ALLOWED_UPDATE_FIELDS
from ..functions.process_delete_product import process_delete_product
from ..models import UserProduct
from ..serializers import UserProductSerializer
from ..serializers.sample_product import SPUserProductSerializer

logger = logging.getLogger(__name__)


class UserProductViewSet(SearchableListModelMixin,
                         mixins.RetrieveModelMixin,
                         AuthenticatedGenericViewSet):
    queryset = UserProduct.objects.status_exclude().order_by('-update_time')
    serializer_class = UserProductSerializer
    filterset_class = UserProductFilter
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = ['id', 'user', 'title', 'description', 'product', 'preview_image_url', 'create_time',
                       'update_time']

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.pk)

    def get_list_queryset(self):
        return self.get_queryset().prefetch_related(
            Prefetch(
                "shop_user_product_set",
                queryset=ShopUserProduct.objects.filter(is_active=True)
            ),
            'shop_user_product_set__shop',
            'shop_user_product_set__shop__ecommerce',
            'shop_user_product_set__shop__currency',
            'user_product_variant_set',
            'user_product_variant_set__abstract_variant',
            'user_product_variant_set__order_items'
        ).annotate(
            order_item_quantity=Sum('user_product_variant_set__order_items__quantity'),
            order_item_count=Count('user_product_variant_set__order_items'))

    def get_detail_queryset(self):
        return self.get_queryset().prefetch_related(
            Prefetch(
                "user_product_variant_set",
                queryset=UserVariant.objects.filter(is_active=True)
            ),
            Prefetch(
                "shop_user_product_set",
                queryset=ShopUserProduct.objects.filter(is_active=True)
            ),
            'user_product_variant_set__abstract_variant',
            'user_product_variant_set__abstract_variant__attributes_value',
            'user_product_variant_set__abstract_variant__attributes_value__attribute',
            'user_product_variant_set__prices',
            'user_product_variant_set__mockup_per_side',
            'user_product_variant_set__order_items',
            'shop_user_product_set__shop',
            'shop_user_product_set__shop__ecommerce',
            'shop_user_product_set__shop__currency',
            # 'artwork_set',
            Prefetch(
                "artwork_set",
                queryset=UserProductArtworkFusion.objects.all()
            ),
            'artwork_set__product_side',
            'artwork_set__artwork_fusion',
            "abstract_product",
            "abstract_product__child_attributes",
            "abstract_product__child_attributes__child_attributes_value_set"
        )

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        logger.info('Querries count: {}'.format(len(connection.queries)))
        return response

    def get_detail_active_only_variant_queryset(self):
        return self.get_queryset().prefetch_related(
            Prefetch(
                "user_product_variant_set",
                queryset=UserVariant.objects.filter(is_active=True, abstract_variant__is_active=True)
            ),
            Prefetch(
                "shop_user_product_set",
                queryset=ShopUserProduct.objects.filter(is_active=True)
            ),
            'user_product_variant_set__abstract_variant',
            'user_product_variant_set__abstract_variant__attributes_value',
            'user_product_variant_set__abstract_variant__attributes_value__attribute',
            'user_product_variant_set__prices',
            'user_product_variant_set__mockup_per_side',
            'shop_user_product_set__shop',
            'shop_user_product_set__shop__ecommerce',
            'shop_user_product_set__shop__currency',
            Prefetch(
                "artwork_set",
                queryset=UserProductArtworkFusion.objects.is_visible()
            ),
            'artwork_set__product_side',
            'artwork_set__artwork_fusion',
            "abstract_product__child_attributes__child_attributes_value_set"
        )

    @staticmethod
    def get_abstract_product_query_set():
        return AbstractProduct.objects.select_related("meta") \
            .prefetch_related(
            Prefetch(
                "abstract_product_variants",
                queryset=AbstractProductVariant.objects
                    .prefetch_related("attributes_value"),
            ),
            Prefetch(
                "child_attributes",
                queryset=ProductAttribute.objects.order_by('sort_index')
                    .prefetch_related(
                    Prefetch(
                        "child_attributes_value_set",
                        queryset=ProductAttributeValue.objects.filter(is_active=True).order_by('sort_index'),
                    )),
            ),
            'mockup_infos',
            'sides'
        )

    error_messages = {
        **to_standard_error_messages(UserProduct.ATTRIBUTE_LABELS)
    }

    def list(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        ids = request.query_params.get("ids")
        queryset = self.get_list_queryset().product_only()
        # .annotate(order_item_count=Count('user_product_variant_set'))
        self.queryset = queryset

        if ids:
            ids = [int(x) for x in ids.split(',')][:100]
            self.queryset = queryset.filter(id__in=ids)
        if q:
            # todo fix search here
            self.queryset = queryset.filter(tsv_metadata_search=q)

        return super().list(request, *args, **kwargs)

    @action(methods=["GET"], detail=False, url_path="brief")
    def list_brief_user_product(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        queryset = self.filter_queryset(self.get_list_queryset())

        if q:
            # todo fix search here
            queryset = queryset.filter(tsv_metadata_search=q)

        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = BriefUserProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = BriefUserProductSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="brief-variants")
    def list_user_product_with_variant(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        queryset = self.filter_queryset(self.get_list_queryset())

        if q:
            # todo fix search here
            queryset = queryset.filter(tsv_metadata_search=q)

        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = UserProductWithVariantsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserProductWithVariantsSerializer(instance=queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        user_product = self.get_detail_queryset().get(id=kwargs['pk'])
        return Response(UserProductDetailSerializer(user_product).data)

    @action(methods=["GET"], detail=True, url_path="async")
    def retrieve_async_info(self, request, *args, **kwargs):
        user_product = self.get_detail_queryset().get(id=kwargs['pk'])
        return Response(UserProductAsyncInfoSerializer(user_product).data)

    @action(methods=["GET"], detail=True, url_path="with_abstract")
    def get_with_abstract(self, request, *args, **kwargs):
        user_product = self.get_detail_queryset().get(id=kwargs['pk'])
        abstract_product = self.get_abstract_product_query_set().get(id=user_product.abstract_product_id)
        return Response({
            "success": True,
            "user_product": UserProductDetailSerializer(user_product).data,
            "abstract_product": ProductSerializer(abstract_product).data,
        })

    @action(methods=["GET"], detail=True, url_path="duplicate")
    def duplicate_product(self, request, *args, **kwargs):
        user_product = self.get_detail_queryset().get(id=kwargs['pk'])
        if user_product.can_duplicate:
            queryset = AbstractProduct.objects.all()
            abstract_product = retrieve_abstract_product(user_product.abstract_product_id, queryset)
            return Response({
                "success": True,
                "user_product": SPUserProductSerializer(instance=user_product).data,
                "abstract_product": abstract_product,
                "mockup_version": user_product.mockup_version
            })
        else:
            return Response({"success":False}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["POST"], detail=True, url_path="add_shop")
    def add_to_shop(self, request, *args, **kwargs):
        shop_ids = request.data["shop_ids"]
        user_product = self.get_object()
        shops = Shop.objects.filter(id__in=shop_ids, owner=self.request.user.pk).exclude(
            user_product_set__user_product_id=user_product.id)
        shop_user_products = ShopUserProduct.objects.bulk_create(
            [ShopUserProduct(shop=shop, user_product=user_product) for shop in shops])
        for shop_user_product in shop_user_products:
            create_product_in_shop_task.delay(shop_user_product.id)
        return Response({"success": True})

    @action(methods=["POST"], detail=True, url_path="resync")
    def re_sync_product(self, request, *args, **kwargs):
        shop_id = request.data["shop_id"]
        try:
            with transaction.atomic():
                user_product = self.get_object()
                user_product.status = UserProductStatus.ACTIVE
                user_product.save()
                for shop_user_product in ShopUserProduct.objects.filter(shop_id=shop_id, user_product=user_product):
                    shop_user_product.is_active = False
                    shop_user_product.save()
                shop = Shop.objects.is_active().get(id=shop_id, owner=self.request.user.pk)
                shop_user_product = ShopUserProduct.objects.create(shop=shop, user_product=user_product,
                                                                   sync_status=ShopUserProductSyncStatus.SYNCING)
                create_product_in_shop(shop_user_product)
                return Response({"success": True,
                                 "message": "Re-Sync product {} in store {} successfully".format(user_product.title,
                                                                                                 shop.name)})
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.info(str(e))

    @action(methods=["POST"], detail=True, url_path="bulk-resync")
    def re_sync_product_all_shop(self, request, *args, **kwargs):
        shop_ids = request.data["shop_ids"]
        try:
            with transaction.atomic():
                user_product = self.get_object()
                user_product.status = UserProductStatus.ACTIVE
                user_product.save()
            bulk_resync_product_task.delay(user_product.id, shop_ids)
            return Response({"success": True,
                             "message": "Product {} is resyncing in all shops".format(user_product.title)})
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.info(str(e))

    @action(methods=["GET"], detail=True, url_path="mockups")
    def get_mockups(self, request, *args, **kwargs):
        user_product = self.get_object()
        mockups = UserVariantSideMockup.objects.only("mockup_url").filter(
            user_variant__user_product__id=user_product.id)
        mockup_urls = []
        for mockup in mockups:
            mockup_urls.append(mockup.mockup_url)
        return Response({"success": True, "mockups": mockup_urls})

    @action(methods=["POST"], detail=False, url_path="push-all-to-shop")
    def push_all_to_shop(self, request, *args, **kwargs):
        shop_id = request.data["shop_id"]
        source_shop_ids = request.data["source_shops"]
        shop = Shop.objects.filter(pk=shop_id, owner=self.request.user.pk).is_active().first()
        source_shops = Shop.objects.filter(id__in=source_shop_ids, owner=self.request.user.pk)
        if shop is not None and len(source_shops) > 0:
            user_products = UserProduct.objects \
                .filter(user=self.request.user.pk, shop_user_product_set__shop__in=source_shops) \
                .exclude(shop_user_product_set__shop=shop)
            shop_user_products = ShopUserProduct.objects.bulk_create(
                [ShopUserProduct(shop=shop, user_product=user_product) for user_product in user_products])
            for shop_user_product in shop_user_products:
                sync_product_in_shop_task.delay(shop_user_product.id)
            return Response({
                "success": True,
                "synced_product_count": len(user_products)
            })
        else:
            return Response({
                "success": True,
                "message": "Shop or Source Shop is not found"
            })

    def update(self, request, *args, **kwargs):
        request_data = request.data
        has_new_variant = False
        need_to_sync_shop = False
        with transaction.atomic():
            user_product = self.get_object()
            if any(field in request_data for field in ALLOWED_UPDATE_FIELDS):
                user_product_update_form = UserProductUpdateForm(request_data, instance=user_product)
                user_product_update_form.validate()
                user_product_update_form.save()
                need_to_sync_shop = True
            if 'variants' in request_data:
                need_to_sync_shop = True
                user_product.user_product_variant_set.all().update(is_active=False)
                variant_ids = []
                currencies = {}

                for sort_index, variant in enumerate(request_data['variants']):
                    if 'id' in variant:
                        variant_obj = user_product.user_product_variant_set.filter(pk=variant['id']).first()
                    elif 'abstract_variant' not in variant:
                        abstract_variant_id = variant["abstract_variant"]
                        variant_obj = user_product.user_product_variant_set.filter(
                            abstract_variant_id=abstract_variant_id).first()
                        if variant_obj is None:
                            abstract_variant = user_product.abstract_product.abstract_product_variants.get(
                                id=abstract_variant_id)
                            if abstract_variant is not None:
                                variant_obj = UserVariant.objects.create(user_product=user_product,
                                                                         abstract_variant=abstract_variant,
                                                                         sort_index=sort_index)
                                variant_obj.sku = variant_obj.id
                                variant_obj.save()
                                has_new_variant = True
                            else:
                                continue
                    else:
                        continue
                    variant_obj.sort_index = sort_index
                    variant_obj.save()
                    for currency, value in variant['price'].items():
                        if currency not in currencies:
                            currencies[currency] = CurrencyExchangeRate.objects.get(pk=currency)
                        UserVariantPrice.objects.update_or_create(currency=currency,
                                                                  user_variant=variant_obj,
                                                                  defaults={
                                                                      "value": value['value'],
                                                                  })
                    variant_ids.append(variant_obj.id)
                user_product.user_product_variant_set.filter(id__in=variant_ids).update(is_active=True)
                # Has no variant, just update preview image by order
                if not has_new_variant:
                    # Re-update preview image
                    first_variant = user_product.user_product_variant_set.filter(is_active=True).order_by(
                        'sort_index').first()
                    user_product.preview_image_url = first_variant.get_preview_mockup()
                    user_product.save(update_fields=['preview_image_url'])

        # call async after transaction to avoid inconsistency
        if has_new_variant:
            logger.info("Regenerate mockup")
            # TODO temp disable feature regenerate mockup
            # process_product_mockup_task.delay(user_product.id, False)
        elif need_to_sync_shop:
            update_user_product_in_all_shop_task.delay(user_product.id)

        user_product = self.get_detail_queryset().get(id=kwargs['pk'])
        return Response({"success": True, "data": UserProductDetailSerializer(instance=user_product).data})

    def destroy(self, request, *args, **kwargs):
        request_data = request.data
        shop_user_product_ids = request_data['shopUserProductIds']
        deep_delete = request_data['deepDelete']
        user_product = self.get_object()

        if deep_delete:
            user_product.status = UserProductStatus.INACTIVE
            user_product.save()

        shop_user_product_synced = []
        shop_user_product_objs = []
        for shop_user_product in ShopUserProduct.objects.filter(id__in=shop_user_product_ids):
            if shop_user_product.is_synced:
                shop_user_product.sync_status = ShopUserProductSyncStatus.PENDING_DELETE
                shop_user_product_synced.append(shop_user_product.id)
            else:
                shop_user_product.sync_status = ShopUserProductSyncStatus.DELETED
            shop_user_product_objs.append(shop_user_product)
        ShopUserProduct.objects.bulk_update(shop_user_product_objs, ['sync_status'])
        process_delete_product.delay(shop_user_product_synced)
        return Response({"is_active": False, "success": True})

    @action(methods=["GET"], detail=True, url_path="variant-list")
    def user_product_with_variants(self, request, *args, **kwargs):
        user_product = self.get_object()
        response = retrieve_user_product_variant_with_pricing(user_product)
        return Response({"success": True, "data": response})

    # @action(methods=["POST"], detail=True, url_path="to-sample", permission_classes=[IsAdminUser])
    # def verify_store(self, request, *args, **kwargs):
    #     user_product = self.get_object()
    #     sample_product, success = create_sample_product(user_product)
    #     return Response({"success": success, "sample_product_id": sample_product})

    @action(methods=['delete'], detail=True, url_path='permanently-delete')
    def permanently_delete(self, request, *args, **kwargs):
        user_product = self.get_object()
        if user_product.abstract_product.type in PRODUCT_DESTROYABLE_TYPE:
            user_settings = user_product.user.settings
            variant_ids = UserVariant.objects.filter(user_product=user_product)
            if user_settings.default_branding_card in variant_ids:
                user_settings.default_branding_card = None
                user_settings.save()
            # UserVariant.objects.filter(id__in=variant_ids).delete()
            user_product.set_status(UserProductStatus.INACTIVE)
            return Response({'success': True})
        else:
            return Response({'success': False, 'message': "Can't delete this product"})
