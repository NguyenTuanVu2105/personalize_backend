import logging
import os

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.caches import redis_cache
from HUB.helpers.model_helper import update_object
from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from abstract_product.constants import ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX
from abstract_product.filters.abstract_product import AdminAbstractProductFilter
from abstract_product.functions.refresh_cached_category_products import refresh_cached_category_products
from abstract_product.models import AbstractProduct, CategoryProduct
from abstract_product.serializers import ProductBasicInfoSerializer
from abstract_product.serializers.admin_abstract_product import AdminAbstractProductSerializer, \
    AdminAbstractProductSimpleSerializer, AdminAbstractProductPreviewAndTemplateSerializer, \
    AdminAbstractProductSortingListSerializer
from abstract_product.services import upload_preview_thumbnail, upload_sample_mockups, upload_design_template, \
    upload_product_side_background, upload_png_design_template
from abstract_product.tasks import cache_abstract_products_task

logger = logging.getLogger(__name__)

User = get_user_model()


class AdminAbstractProductViewSet(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.ListModelMixin,
                                  AdminGenericViewSet):
    queryset = AbstractProduct.objects.all().order_by('-is_active', 'sort_index')
    serializer_class = AdminAbstractProductSerializer
    # filterset_fields = ['title', 'categories', 'is_active']
    filterset_class = AdminAbstractProductFilter
    error_messages = {}

    @method_permission_required(get_permissions(['admin_abstract_product_view', ]))
    def list(self, request, *args, **kwargs):
        # data = self.filter_queryset(queryset=self.queryset)
        # return Response(AdminAbstractProductSerializer(data, many=True).data)
        response = super().list(request, *args, **kwargs)
        response_data = response.data
        abstract_queryset = AbstractProduct.objects.filter(~Q(sku=None)).order_by("sku", "-update_time").only(
            'id', 'title', 'sku', 'is_active', 'preview_image_url').distinct("sku")
        response_data["abstracts"] = ProductBasicInfoSerializer(abstract_queryset, many=True).data
        return response

    @action(methods=['GET'], detail=False, url_path='all',
            permission_classes=get_permissions(['admin_abstract_product_view']))
    def get_all(self, request, *args, **kwargs):
        data = self.filter_queryset(queryset=self.queryset)
        return Response(AdminAbstractProductSimpleSerializer(data, many=True).data)

    @method_permission_required(get_permissions(['admin_abstract_product_view', ]))
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related("meta").prefetch_related(
            'abstract_product_variants',
            'abstract_product_variants__attributes_value',
            'abstract_product_variants__attributes_value__attribute',
            'child_attributes__child_attributes_value_set',
            'child_attributes__child_attributes_value_set__attribute',
            'mockup_infos',
            'sides'
        )
        product = queryset.get(pk=kwargs['pk'])
        return Response(AdminAbstractProductSerializer(product).data)

    @method_permission_required(get_permissions(['admin_abstract_product_update', ]))
    def update(self, request, *args, **kwargs):
        request_data = request.data
        with transaction.atomic():
            abstract_product = self.get_object()

            update_object(abstract_product, request_data,
                          ['title', 'is_active', 'is_catalog_visible', 'active_mockup_version'])
            redis_cache.delete_pattern(pattern=ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX + '*')
            abstract_product.save()

            if 'meta' in request_data:
                abstract_product_meta = abstract_product.meta
                update_object(abstract_product_meta, request_data['meta'],
                              ['base_cost', 'short_description', 'description', 'shipping_meta', 'pricing_meta',
                               'design_note', 'fusion_meta'])
                abstract_product_meta.save()

            if 'sides' in request_data:
                for side_data in request_data["sides"]:
                    abstract_product_side = abstract_product.sides.filter(pk=side_data['id']).first()
                    update_object(abstract_product_side, side_data, ['type', 'constraints'])
                    abstract_product_side.save()

            if 'mockup_infos' in request_data:
                for mockup_info_data in request_data['mockup_infos']:
                    mockup_info = abstract_product.mockup_infos.filter(pk=mockup_info_data['id']).first()
                    update_object(mockup_info, mockup_info_data, ['meta', 'preview', 'preview_meta'])
                    mockup_info.save()

            if 'abstract_product_variants' in request_data:
                for abstract_product_variant_data in request_data['abstract_product_variants']:
                    abstract_product_variant = abstract_product.abstract_product_variants.filter(
                        pk=abstract_product_variant_data['id']).first()
                    update_object(abstract_product_variant, abstract_product_variant_data,
                                  ['base_cost', 'mockup_info_id'])
                    abstract_product_variant.save()

            if 'child_attributes' in request_data:
                for child_attribute_data in request_data['child_attributes']:
                    child_attribute = abstract_product.child_attributes.filter(
                        pk=child_attribute_data['id']).first()
                    update_object(child_attribute, child_attribute_data, ['name', 'select_type'])
                    child_attribute.save()
                    if 'child_attributes_value_set' in child_attribute_data:
                        print(child_attribute)
                        for child_attribute_value_data in child_attribute_data['child_attributes_value_set']:
                            child_attribute_value = child_attribute.child_attributes_value_set.filter(
                                pk=child_attribute_value_data['id']).first()
                            update_object(child_attribute_value, child_attribute_value_data, ['value', 'is_active'])
                            child_attribute_value.save()

            if 'categories' in request_data:
                CategoryProduct.objects.filter(product=abstract_product).delete()
                for category_data in request_data['categories']:
                    CategoryProduct.objects.update_or_create(product=abstract_product,
                                                             category_id=category_data['id'])
            cache_abstract_products_task.delay(abstract_product.id)
        return Response({"success": True, "message": "Update Basic info successfully"})

    @action(methods=["GET"], detail=True, url_path="template-meta",
            permission_classes=get_permissions(['admin_abstract_product_view']))
    def retrieve_template_meta(self, request, *args, **kwargs):
        abstract_product = self.get_object()
        template_meta = AdminAbstractProductPreviewAndTemplateSerializer(abstract_product).data
        return Response({"success": True, "data": template_meta})

    @action(methods=["POST"], detail=True, url_path="upload-preview-thumbnail",
            permission_classes=get_permissions(['admin_abstract_product_update']))
    def upload_preview_thumbnail(self, request, *args, **kwargs):
        abstract_product = self.get_object()
        # TODO DELETE OLD FILE IN STORAGE
        success, file_url = upload_preview_thumbnail(abstract_product, request)
        return Response({"success": success, "file_url": file_url})

    @action(methods=["POST"], detail=True, url_path="upload-design-template",
            permission_classes=get_permissions(['admin_abstract_product_update']))
    def upload_design_template(self, request, *args, **kwargs):
        abstract_product = self.get_object()
        # TODO DELETE OLD FILE IN STORAGE
        # logger.info("REQQQQQQQQQQQQQQQQQQQQ")
        # logger.info(request.FILES['template'])
        # logger.info(request.FILES['template'].name)
        logger.info(os.path.splitext(request.FILES['template'].name)[1].strip("."))
        success, template_meta = upload_design_template(abstract_product, request.FILES['template'])
        return Response({"success": success, "template_meta": template_meta})

    @action(methods=["POST"], detail=True, url_path="png-template",
            permission_classes=get_permissions(['admin_abstract_product_update']))
    def upload_png_template(self, request, *args, **kwargs):
        abstract_product = self.get_object()
        # TODO DELETE OLD FILE IN STORAGE
        # logger.info(os.path.splitext(request.FILES['template'].name)[1].strip("."))
        success, file_url = upload_png_design_template(abstract_product, request.FILES['template'])
        return Response({"success": success, "file_url": file_url})

    @action(methods=["POST"], detail=True, url_path="upload-sample-mockups",
            permission_classes=get_permissions(['admin_abstract_product_update']))
    def upload_sample_mockups(self, request, *args, **kwargs):
        abstract_product = self.get_object()
        # TODO DELETE OLD FILE IN STORAGE
        success, template_meta = upload_sample_mockups(abstract_product, request.data.getlist('unchanged_mockups'),
                                                       request.FILES.getlist('add_mockups'))
        return Response({"success": success, "template_meta": template_meta})

    @action(methods=["POST"], detail=True, url_path="upload-product-side-background",
            permission_classes=get_permissions(['admin_abstract_product_update']))
    def upload_product_side_background(self, request, *args, **kwargs):
        abstract_product = self.get_object()
        side_type = request.data.get('side_type')
        request_files = request.FILES
        background_image = request_files.get('background_image')
        success, preview_data = upload_product_side_background(abstract_product, side_type, background_image)
        return Response({'success': success, 'preview_data': preview_data})

    @action(methods=["GET"], detail=False, url_path="sorting-list",
            permission_classes=get_permissions(['admin_abstract_product_view']))
    def get_sorting_product_list(self, request, *args, **kwargs):
        data = self.queryset.filter(is_active=True)
        return Response(AdminAbstractProductSortingListSerializer(data, many=True).data)

    @action(methods=["POST"], detail=False, url_path="sorting",
            permission_classes=get_permissions(['admin_abstract_product_update']))
    def sort_product(self, request, *args, **kwargs):
        request_data = request.data
        try:
            products = request_data
            for index, product_id in enumerate(products):
                product = AbstractProduct.objects.get(id=product_id)
                product.sort_index = index + 1
                product.save()

            refresh_cached_category_products()

        except Exception as e:
            print(str(e))
            return Response({"success": False, "message": str(e)})
        else:
            return Response({"success": True, "message": "Reorder category successfully"})
