import logging

import django_filters
from django.db import transaction
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from HUB.permissions import get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from user_product.constants import SampleProductStatus
from user_product.filters import AdminSampleProductFilter
from user_product.functions.sample_product import update_sample_product
from user_product.models import SampleProduct
from user_product.serializers import SampleProductSerializer, AdminSampleProductDetailSerializer
from user_product.serializers.sample_product import AdminSampleProductListSerializer

logger = logging.getLogger(__name__)


class AdminSampleProductViewSet(SearchableListModelMixin,
                                UpdateModelMixin,
                                AdminGenericViewSet):
    queryset = SampleProduct.objects.all().order_by('-create_time')
    serializer_class = SampleProductSerializer
    filterset_class = AdminSampleProductFilter
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = ['id', 'create_time', 'update_time']

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        queryset = self.filter_queryset(self.get_queryset())

        if q:
            # todo fix search here
            queryset = queryset.filter(tsv_metadata_search=q)

        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = AdminSampleProductDetailSerializer(page, many=True)
            abstract_product_options = self.get_queryset().order_by() \
                .distinct('original_product__abstract_product__id') \
                .values('original_product__abstract_product__id', 'title')
            owner_options = self.get_queryset().order_by() \
                .distinct('original_product__user') \
                .values('original_product__user__id',
                        'original_product__user__name')
            response = self.get_paginated_response(serializer.data).data
            response['options'] = {'abstract_product': abstract_product_options, 'owner': owner_options}
            return Response(response)
        serializer = AdminSampleProductDetailSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        request_data = request.data
        with transaction.atomic():
            sample_product = self.get_object()
            sample_product.detail_data = request_data
            sample_product.title = request_data['title']
            sample_product.preview_image_url = request_data['preview_image_url']
            sample_product.save()
        return Response({'success': True})

    @action(methods=["DELETE"], detail=False, url_path="bulk-delete")
    def bulk_delete(self, request, *args, **kwargs):
        request_data = request.data
        product_id_list = request_data['ids']
        response_data = []
        for id in product_id_list:
            sample_product = SampleProduct.objects.get(pk=id)
            sample_product.delete()
            response_data.append({
                "sample_product": id,
                "success": True
            })
        return Response({"results": response_data})

    @action(methods=["DELETE"], detail=False, url_path="bulk-deactive")
    def bulk_deactive(self, request, *args, **kwargs):
        request_data = request.data
        product_id_list = request_data['ids']
        response_data = []
        for id in product_id_list:
            sample_product = SampleProduct.objects.get(pk=id)
            sample_product.status = SampleProductStatus.INACTIVE
            sample_product.save()
            response_data.append({
                "sample_product": id,
                "success": True
            })
        return Response({"results": response_data})

    @action(methods=["POST"], detail=False, url_path="bulk-active")
    def bulk_active(self, request, *args, **kwargs):
        request_data = request.data
        product_id_list = request_data['ids']
        response_data = []
        for id in product_id_list:
            sample_product = SampleProduct.objects.get(pk=id)
            sample_product.status = SampleProductStatus.ACTIVE
            sample_product.save()
            response_data.append({
                "sample_product": id,
                "success": True
            })
        return Response({"results": response_data})

    @action(methods=["POST"], detail=False, url_path="bulk-enable-highlight")
    def bulk_enable_highlight(self, request, *args, **kwargs):
        request_data = request.data
        product_id_list = request_data['ids']
        response_data = []
        SampleProduct.objects.all().update(is_highlight=False)
        for id in product_id_list:
            sample_product = SampleProduct.objects.get(pk=id)
            sample_product.is_highlight = True
            sample_product.save()
            response_data.append({
                "sample_product": id,
                "success": True
            })
        return Response({"results": response_data})

    @action(methods=["GET"], detail=False, url_path="highlight-list",
            permission_classes=get_permissions(['admin_highlight_product_view']))
    def get_highlight_list(self, request, *args, **kwargs):
        queryset = SampleProduct.objects.is_highlight()
        serializer = AdminSampleProductListSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="normal-list",
            permission_classes=get_permissions(['admin_highlight_product_view']))
    def get_normal_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.is_not_highlight()
        serializer = AdminSampleProductListSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False, url_path="refresh",
            permission_classes=get_permissions(['admin_highlight_product_update']))
    def refresh_data(self, request, *args, **kwargs):
        request_data = request.data
        sample_list = request_data['sample_ids']
        succeed_count = 0
        for sample_id in sample_list:
            sample_product = SampleProduct.objects.get(pk=sample_id)
            succeed = update_sample_product(sample_product)
            if succeed:
                succeed_count = succeed_count + 1
        return Response({"success": True, "message": f"Success {succeed_count}/{len(sample_list)} sample products"})
