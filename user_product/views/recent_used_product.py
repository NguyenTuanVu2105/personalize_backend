from django.db.models import Subquery
from rest_framework.response import Response

from HUB.caches import get_cached_object
from HUB.viewsets.base import BaseGenericAPIView
from abstract_product.constants import ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX, ABSTRACT_PRODUCT_CACHE_TIMEOUT
from abstract_product.models import AbstractProductCategory
from abstract_product.querysets import abstract_product_category_queryset
from abstract_product.serializers import AbstractProductCategorySerializer
from abstract_product.serializers.brief_abstract_product import BriefAbstractProductSerializer
from abstract_product.tasks import cache_object_if_not_exist_task
from ..models import UserProduct


class RecentUsedProductView(BaseGenericAPIView):
    error_messages = {
        "product": {
            "invalid": "This product is invalid",
        }
    }

    def get_queryset(self):
        return UserProduct.objects.filter(id__in=Subquery(
            UserProduct.objects.filter(user_id=self.request.user.pk, abstract_product__is_active=True,
                                       abstract_product__is_catalog_visible=True).exclude(
                abstract_product__id=None).distinct(
                "abstract_product__id").order_by("-abstract_product__id", "-id").values_list('id',
                                                                                             flat=True))).order_by(
            "-create_time") \
                   .select_related('abstract_product',
                                   'abstract_product__meta') \
                   .prefetch_related('abstract_product__categories',
                                     'abstract_product__child_attributes',
                                     'abstract_product__child_attributes__child_attributes_value_set')[:12]

    def get(self, request):
        base_category_queryset = AbstractProductCategory.objects.all()
        category_queryset = abstract_product_category_queryset(base_category_queryset)
        popular_category = category_queryset.filter(title="Popular").first()
        cache_key = ABSTRACT_PRODUCT_CATEGORY_CACHE_KEY_PREFIX + str(popular_category.id)
        cached_object = get_cached_object(cache_key)
        if cached_object:
            popular_response = cached_object
        else:
            popular_response = AbstractProductCategorySerializer(popular_category).data

            cache_object_if_not_exist_task.delay(cache_key, popular_response, ABSTRACT_PRODUCT_CACHE_TIMEOUT)
        user_products_queryset = self.get_queryset()
        result = []
        for user_product in user_products_queryset:
            product = user_product.abstract_product
            result.append(BriefAbstractProductSerializer(instance=product).data)
        abstract_recent_ids = [x['id'] for x in result]
        for abstract_product in popular_response['child_abstract_products']:
            if abstract_product['id'] not in abstract_recent_ids:
                result.append(abstract_product)
        # serializer = ProductListSerializer(result, many=True)
        # return Response(serializer.data)
        response = {
            "id": 0,
            "child_abstract_products": result,
            "description": "Recommend",
            "sort_index": 0,
            "is_active": True
        }
        return Response({"success": True, "data": response})
