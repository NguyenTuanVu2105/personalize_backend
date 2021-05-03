import logging
import traceback

from django.db import transaction
from django.db.models import Q
from rest_framework import mixins, status
from rest_framework.response import Response

from HUB.permissions import IsAuthenticated, method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from abstract_product.forms import AbstractCategoryForm
from abstract_product.models import AbstractProductCategory, CategoryProduct
from abstract_product.serializers import AbstractProductCategorySerializer
from abstract_product.serializers.brief_abstract_product_category import BriefAbstractProductCategorySerializer

logger = logging.getLogger(__name__)


class AdminAbstractProductCategoryViewSet(mixins.ListModelMixin,
                                          mixins.RetrieveModelMixin,
                                          AdminGenericViewSet):
    permission_classes = [IsAuthenticated]

    queryset = AbstractProductCategory.objects.all().order_by('-sort_index')
    serializer_class = BriefAbstractProductCategorySerializer
    filterset_fields = ['title', 'is_active']
    search_fields = 'title'
    ordering_fields = ['title', 'is_active', 'preview_image_url', 'sort_index']

    def get_queryset(self):
        return self.queryset.all().order_by('-sort_index')

    # @method_decorator(cache_page(5 * 60))
    @method_permission_required(get_permissions(['admin_abstract_product_category_view', ]))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BriefAbstractProductCategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BriefAbstractProductCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_required(get_permissions(['admin_abstract_product_category_view', ]))
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().prefetch_related('child_abstract_products',
                                                        'child_abstract_products__meta',
                                                        'child_abstract_products__categories',
                                                        'child_abstract_products__child_attributes',
                                                        'child_abstract_products__child_attributes__child_attributes_value_set')
        category = queryset.get(pk=kwargs['pk'])
        return Response(AbstractProductCategorySerializer(category).data)

    @method_permission_required(get_permissions(['admin_abstract_product_category_update', ]))
    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                category = self.get_object()
                request_data = request.data
                if 'title' in request_data:
                    category.title = request_data['title']
                if 'products' in request_data:
                    product_list = request_data['products']
                    category.product_category_set.filter(~Q(product_id__in=product_list)).delete()
                    for product_id in product_list:
                        CategoryProduct.objects.get_or_create(product_id=product_id, category=category)
                if 'is_active' in request_data:
                    category.is_active = request_data['is_active']

                category.save()
                return Response({"success": True, "message": f"Update {category.title} category successfully"})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})

    @method_permission_required(get_permissions(['admin_abstract_product_category_update', ]))
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                request_data = request.data
                form = AbstractCategoryForm(data=request_data)
                if form.is_valid():
                    category_amount = AbstractProductCategory.objects.count()
                    category = AbstractProductCategory.objects.create(title=request_data['title'], is_active=True,
                                                                      sort_index=category_amount + 1)
                    product_list = request_data['product_list']
                    for product_id in product_list:
                        CategoryProduct.objects.get_or_create(product_id=product_id, category=category)
                else:
                    errors = [error for error in form.errors]
                    return Response(data={"success": False, 'message': 'This fields is required:  {}'.format(errors)},
                                    status=status.HTTP_200_OK)

                return Response({"success": True, "message": f"Create {category.title} category successfully"})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})

    @method_permission_required(get_permissions(['admin_abstract_product_category_update', ]))
    def delete(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                category = self.get_object()
                category.product_category_set.all().delete()
                category.delete()
                return Response({"success": True, "message": f"Delete {category.title} category successfully"})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})
