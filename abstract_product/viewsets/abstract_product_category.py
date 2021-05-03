import logging

from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework.response import Response

from HUB.caches import get_cached_object
from HUB.permissions import IsAuthenticated
from HUB.viewsets.base import AuthenticatedGenericViewSet
from abstract_product.constants import ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CACHE_TIMEOUT
from abstract_product.models import AbstractProductCategory, AbstractProduct
from abstract_product.querysets import abstract_product_category_queryset
from abstract_product.serializers import AbstractProductCategorySerializer
from abstract_product.serializers.brief_abstract_product_category import BriefAbstractProductCategorySerializer
from abstract_product.tasks import cache_object_if_not_exist_task

logger = logging.getLogger(__name__)


class AbstractProductCategoryViewSet(mixins.ListModelMixin,
                                     mixins.RetrieveModelMixin,
                                     AuthenticatedGenericViewSet):
    permission_classes = [IsAuthenticated]

    queryset = AbstractProductCategory.objects.filter(is_active=True).order_by('-sort_index')
    serializer_class = BriefAbstractProductCategorySerializer
    filterset_fields = ['title']
    search_fields = 'title'
    ordering_fields = ['title', 'preview_image_url', 'sort_index']

    def get_queryset(self):
        return self.queryset.exclude(title="Popular").order_by('-force_active', '-sort_index')

    def retrieve(self, request, *args, **kwargs):
        category_id = str(kwargs['pk'])
        cache_key = ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX + category_id
        cached_object = get_cached_object(cache_key)

        if cached_object:
            return Response(cached_object)

        else:
            queryset = abstract_product_category_queryset(self.get_queryset())
            category = queryset.get(pk=kwargs['pk'])
            response_data = AbstractProductCategorySerializer(category).data
            cache_object_if_not_exist_task.delay(cache_key, response_data, ABSTRACT_PRODUCT_CACHE_TIMEOUT)

            return Response(response_data)
