import logging

import django_filters
from django.db.models import Prefetch, Count
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from abstract_product.functions import retrieve_abstract_product
from abstract_product.functions.retrieve_product_pricing import retrieve_pricing_with_attributes
from abstract_product.models import AbstractProduct, AbstractProductVariant, ProductAttribute, ProductAttributeValue
from user_product.filters import SampleProductFilter
from user_product.models import SampleProduct
from user_product.serializers import SampleProductSerializer, SampleProductListSerializer
from user_product.serializers.sample_product import DetailSampleProductWithAbstractSerializer
from user_product.serializers.sample_product.base import PopularSampleProductSerializer

logger = logging.getLogger(__name__)


class SampleProductViewSet(SearchableListModelMixin,
                           AuthenticatedGenericViewSet):
    queryset = SampleProduct.objects.all().order_by('-create_time')
    serializer_class = SampleProductSerializer
    filterset_class = SampleProductFilter
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = ['id', 'create_time', 'update_time']

    def get_queryset(self):
        return self.queryset.is_active().unused_filter(user=self.request.user.pk)

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

    def list(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        queryset = self.filter_queryset(self.get_queryset())

        if q:
            # todo fix search here
            queryset = queryset.filter(tsv_metadata_search=q)

        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = SampleProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SampleProductListSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=True, url_path="variant-list")
    def get_variant_list(self, request, *args, **kwargs):
        sample_product = self.get_object()
        variant_list = sample_product.variant_list
        for variant in variant_list:
            variant.update({"abstract_variant_data": retrieve_pricing_with_attributes(
                variant['abstract_variant'])})

        return Response({"success": True, "data": sample_product.variant_list})

    @action(methods=["GET"], detail=False, url_path="highlight-list")
    def get_highlight_list(self, request, *args, **kwargs):
        queryset = SampleProduct.objects.is_highlight()[:12]
        serializer = SampleProductListSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=True, url_path="detail")
    def get_product_detail(self, request, *args, **kwargs):
        sample_product = SampleProduct.objects.get(pk=kwargs['pk'])
        serializer = DetailSampleProductWithAbstractSerializer(instance=sample_product)
        return Response(serializer.data)

    @action(methods=["GET"], detail=True, url_path="with-abstract")
    def get_with_abstract(self, request, *args, **kwargs):
        sample_product = SampleProduct.objects.is_highlight().get(pk=kwargs['pk'])
        queryset = AbstractProduct.objects.all()
        # queryset = AbstractProductViewSet().queryset
        abstract_product = retrieve_abstract_product(sample_product.original_product.abstract_product_id, queryset)
        return Response({
            "success": True,
            "sample_product": sample_product.detail_data,
            "abstract_product": abstract_product,
            "mockup_version": sample_product.original_product.mockup_version
        })

    @action(methods=['GET'], detail=False, url_path='popular-products',
            permission_classes=[IsAdminUser])
    def get_popular_sample_product(self, request, *args, **kwargs):
        self.filter_queryset(SampleProduct.objects.all())
        queryset = SampleProduct.objects.annotate(total_created=Count('created_user_products'))\
            .annotate(total_sold=Count('created_user_products__user_product_variant_set__order_items'))\
            .exclude(total_created=0)\
            .order_by('-total_created', '-total_sold')
        return Response({'success': True, 'data': PopularSampleProductSerializer(queryset, many=True).data})
