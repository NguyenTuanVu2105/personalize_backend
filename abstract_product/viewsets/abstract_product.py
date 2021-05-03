import logging

import django_filters
from rest_framework import filters, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.caches import get_cached_object
from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from abstract_product.constants import ABSTRACT_PRODUCT_PRICING_CACHE_KEY_PREFIX, \
    ABSTRACT_PRODUCT_CACHE_TIMEOUT
from abstract_product.functions import retrieve_product_pricing, retrieve_abstract_product
from abstract_product.serializers.brief_abstract_product import BriefAbstractProductSerializer
from abstract_product.tasks import cache_object_if_not_exist_task
from ..models import AbstractProduct

logger = logging.getLogger(__name__)


class AbstractProductViewSet(SearchableListModelMixin,
                             mixins.RetrieveModelMixin,
                             AuthenticatedGenericViewSet):
    queryset = AbstractProduct.objects.active_visible_filter()
    serializer_class = BriefAbstractProductSerializer
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend)
    filterset_fields = ['title', 'categories', 'type']
    ordering_fields = '__all__'

    def retrieve(self, request, *args, **kwargs):
        response_data = retrieve_abstract_product(kwargs['pk'], self.get_queryset())
        return Response(response_data)

    @action(methods=["GET"], detail=True, url_path="cost_details")
    def cost_details(self, request, *args, **kwargs):
        product_id = str(kwargs['pk'])
        cache_key = ABSTRACT_PRODUCT_PRICING_CACHE_KEY_PREFIX + product_id
        cached_object = get_cached_object(cache_key)

        if cached_object:
            return Response(cached_object)
        else:
            response_data = retrieve_product_pricing(product_id=self.kwargs['pk'])
            cache_object_if_not_exist_task.delay(cache_key, response_data, ABSTRACT_PRODUCT_CACHE_TIMEOUT)
            return Response(response_data)

    @action(methods=["POST"], detail=True, url_path="error_log")
    def variant_load_error_log(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        message = request.data['message'] if "message" in request.data else ""
        logger.exception(
            f"Loading Variants Failed: {product.id} - {product.title}. User: {user.pk} - {user.email}. {message}")
        return Response({})
