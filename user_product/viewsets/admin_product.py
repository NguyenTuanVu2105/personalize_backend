import logging
import traceback

import django_filters
from django.contrib.auth import get_user_model
from django.db import connection, transaction
from django.db.models import Prefetch, Sum, Count, Q
from rest_framework import filters, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.helpers.error_messages import to_standard_error_messages
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from abstract_product.models import AbstractProduct, ProductAttributeValue, AbstractProductVariant, ProductAttribute, \
    SKUTemplate
from abstract_product.serializers import ProductBasicInfoSerializer
from abstract_product.serializers.abstract_product_side import BriefSideSerializer
from service_communication.services.mockup_generator_service.artwork_fusion import \
    MockupArtworkFusionCommunicationService
from user.serializers.user import BriefUserSerializer
from user_product.filters import AdminProductFilter
from user_product.functions.sample_product import create_sample_product
from user_product.models import UserVariant, ShopUserProduct, Artwork
from user_product.serializers import AdminProductSerializer
from ..functions.artwork_fusion.generate_combined_artwork_fusion import retrieve_combined_fusion_request_data
from ..functions.artwork_fusion.regenerate_user_product_artwork_fusion import regenerate_user_product_artwork_fusion
from ..functions.artwork_fusion.retrieve_artwork_info import retrieve_layer_info
from ..functions.artwork_fusion.sync_artwork_fusion_info import sync_artwork_fusion_info
from ..models import UserProduct
from ..serializers.admin_product import AdminUserProductDetailSerializer
from ..services.get_user_product_as_xlsx import AdminProductWorkbook

logger = logging.getLogger(__name__)
User = get_user_model()


class AdminProductViewSet(SearchableListModelMixin,
                          mixins.RetrieveModelMixin,
                          AdminGenericViewSet):
    queryset = UserProduct.objects.status_exclude().order_by('-create_time')
    serializer_class = AdminProductSerializer
    filterset_class = AdminProductFilter
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = ['id', 'user', 'title', 'description', 'product', 'preview_image_url', 'create_time',
                       'update_time']

    def get_queryset(self):
        return self.queryset

    def get_list_queryset(self):
        return self.get_queryset().prefetch_related(
            Prefetch(
                "shop_user_product_set",
                queryset=ShopUserProduct.objects.filter(is_active=True)
            ),
            'user',
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
            'artwork_set',
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
            'artwork_set',
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
        queryset = self.get_list_queryset()
        # .annotate(order_item_count=Count('user_product_variant_set'))
        self.queryset = queryset

        if ids:
            ids = [int(x) for x in ids.split(',')][:100]
            self.queryset = queryset.filter(id__in=ids)
        if q:
            # todo fix search here
            self.queryset = queryset.filter(tsv_metadata_search=q)

        response = super().list(request, *args, **kwargs)
        response_data = response.data
        response_data["users"] = BriefUserSerializer(User.objects.all(), many=True).data
        abstract_queryset = AbstractProduct.objects.filter(~Q(sku=None)).order_by("sku", "-update_time").only(
            'id', 'title', 'sku', 'is_active', 'preview_image_url').distinct("sku")
        response_data["abstracts"] = ProductBasicInfoSerializer(abstract_queryset, many=True).data
        return response

    @action(methods=["POST"], detail=True, url_path="to-sample")
    def to_sample(self, request, *args, **kwargs):
        user_product = self.get_object()
        sample_product, success = create_sample_product(user_product)
        return Response({"success": success, "sample_product_id": sample_product})

    @action(methods=["POST"], detail=False, url_path="to-sample")
    def bulk_to_sample(self, request, *args, **kwargs):
        request_data = request.data
        product_id_list = request_data['ids']
        response_data = []
        for id in product_id_list:
            user_product = UserProduct.objects.get(pk=id)
            sample_product, success = create_sample_product(user_product)
            response_data.append({
                "user_product": id,
                "sample_product": sample_product,
                "success": success
            })
        return Response({"results": response_data})

    def retrieve(self, request, *args, **kwargs):
        user_product = self.get_detail_queryset().get(id=kwargs['pk'])
        return Response(AdminUserProductDetailSerializer(user_product).data)

    @action(methods=["POST"], detail=True, url_path="signed-original-fusion")
    def download_original_fusion(self, request, *args, **kwargs):
        user_product = self.get_object()
        request_data = request.data
        artwork_fusion_id = request_data['artwork_fusion_id']
        user_product_artwork_fusion = user_product.artwork_set.filter(artwork_fusion__id=artwork_fusion_id).first()
        if user_product_artwork_fusion:
            artwork_fusion = user_product_artwork_fusion.artwork_fusion
            return Response(
                {"success": True, "signed_original_fusion": artwork_fusion.generate_original_image_signed_url()})
        else:
            return Response({"success": False})

    @action(methods=["POST"], detail=True, url_path="signed-original-artwork")
    def download_original_artwork(self, request, *args, **kwargs):
        request_data = request.data
        artwork_id = request_data['artwork_id']
        artwork = Artwork.objects.filter(id=artwork_id).first()
        if artwork:
            return Response({"success": True, "signed_original_artwork": artwork.generate_original_image_signed_url()})
        else:
            return Response({"success": False})

    @action(methods=["POST"], detail=True, url_path="replace-fusion")
    def replace_fusion(self, request, *args, **kwargs):
        user_product = self.get_object()
        request_data = request.data
        artwork_fusion_id = request_data['artwork_fusion_id']
        fulfill_update = request_data['fulfill_update']
        user_product_artwork_fusion = user_product.artwork_set.filter(artwork_fusion__id=artwork_fusion_id).first()
        if user_product_artwork_fusion:
            artwork_fusion = user_product_artwork_fusion.artwork_fusion
            artwork_fusion.original_image_path = request_data['original_path']
            artwork_fusion.image_url = request_data['thumbnail_url']
            if fulfill_update:
                from user_product.functions.artwork_fusion import push_artwork_fusion
                success, message = push_artwork_fusion(user_product_artwork_fusion, artwork_fusion)
                return Response({"success": success, "message": message})
            else:
                artwork_fusion.save()
                return Response({"success": True,
                                 "message": "Replace artwork fusion successfully!"})

        else:
            return Response({"success": False, "message": "NOT_FOUND"}, status=404)

    @action(methods=["POST"], detail=True, url_path="push-fusion")
    def push_fusion_to_ffm(self, request, *args, **kwargs):
        # Push Fusion To Fulfillment
        user_product = self.get_object()
        request_data = request.data
        artwork_fusion_id = request_data['artwork_fusion_id']
        user_product_artwork_fusion = user_product.artwork_set.filter(artwork_fusion__id=artwork_fusion_id).first()
        if user_product_artwork_fusion:
            artwork_fusion = user_product_artwork_fusion.artwork_fusion
            from user_product.functions.artwork_fusion import push_artwork_fusion
            success, message = push_artwork_fusion(user_product_artwork_fusion, artwork_fusion)
            return Response({"success": success, "message": message})

        else:
            return Response({"success": False, "message": "NOT_FOUND"}, status=404)

    @action(methods=["POST"], detail=False, url_path="regenerate-fusion")
    def regenerate_fusion(self, request, *args, **kwargs):
        try:
            request_data = request.data
            user_product_ids = request_data['user_products']
            regenerate_option = request_data['regenerate_option']
            for user_product_id in user_product_ids:
                user_product = UserProduct.objects.get(id=user_product_id)
                regenerate_user_product_artwork_fusion(user_product, regenerate_option)
            return Response(
                {"success": True,
                 "message": "These artwork fusions will be updated in selected products in few minutes"})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})

    @action(methods=["GET"], detail=True, url_path="retrieve-fusion-info")
    def retrieve_fusion_info(self, request, *args, **kwargs):
        try:
            user_product = self.get_object()
            artwork_fusion = user_product.artwork_set.send_to_fulfill_filter().first().artwork_fusion
            artwork_infos = []
            for artwork_fusion_info in artwork_fusion.artwork_fusion_info_artwork_set.all():
                artwork_data = retrieve_layer_info(artwork_fusion_info.artwork, artwork_fusion_info)
                artwork_infos.append(artwork_data)

            abstract_product = user_product.abstract_product

            user_product_artworks = user_product.artwork_set.all()
            separated_side_user_product_artwork_fusions = user_product_artworks.send_to_fulfill_exclude()
            fulfill_user_product_artwork_fusion = user_product_artworks.send_to_fulfill_filter().first()
            combined_fusion_request_data = retrieve_combined_fusion_request_data(user_product,
                                                                                 separated_side_user_product_artwork_fusions,
                                                                                 fulfill_user_product_artwork_fusion)
            return Response({"success": True, "artwork_infos": artwork_infos,
                             "sides": BriefSideSerializer(instance=abstract_product.sides, many=True).data,
                             "combined_fusion_request_data": combined_fusion_request_data})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})

    @action(methods=["POST"], detail=True, url_path="sync-artwork-info")
    def sync_artwork_info(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                user_product = self.get_object()
                request_data = request.data
                combined_fusion_request_data = request_data['combined_fusion_request_data']
                fulfill_user_product_artwork_fusion = user_product.artwork_set.send_to_fulfill_filter().first()
                MockupArtworkFusionCommunicationService.generate_artwork_fusion(fulfill_user_product_artwork_fusion,
                                                                                combined_fusion_request_data)

                side_fusion_infos = combined_fusion_request_data['side_fusion_infos']
                sync_artwork_fusion_info(user_product, side_fusion_infos)
                # regenerate_user_product_artwork_fusion(user_product)

                return Response({"success": True,
                                 "message": "These artwork fusions will be updated in selected products in few minutes"})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})

    @action(methods=['GET'], detail=False, url_path='export')
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        workbook = AdminProductWorkbook(queryset)
        response = workbook.get_workbook()
        return response

    @action(methods=['GET'], detail=True, url_path='fusion-compare')
    def fusion_compare(self, request, *args, **kwargs):
        user_product = self.get_object()
        abstract_product = user_product.abstract_product
        sku_template = SKUTemplate.objects.filter(sku=abstract_product.sku).first()
        fusion_artworks = user_product.artwork_set.filter(send_to_fulfill=True)
        fusion_list = []
        for user_product_artwork_fusion in fusion_artworks:
            artwork_fusion = user_product_artwork_fusion.artwork_fusion
            side = user_product_artwork_fusion.product_side
            fusion_list.append({"side": side.type, "signed_url": artwork_fusion.generate_original_image_signed_url()})
        return Response({"success": True, "data": {
            "artwork_fusions": fusion_list,
            "fusion_template": sku_template.png_template_url if sku_template else ""
        }})
