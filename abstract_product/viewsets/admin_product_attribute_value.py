from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from abstract_product.models import ProductAttributeValue
from abstract_product.serializers.product_attribute_value import AdminProductAttributeValueSerializer


class AdminProductAttributeValue(AdminGenericViewSet, RetrieveModelMixin, ListModelMixin, UpdateModelMixin):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = AdminProductAttributeValueSerializer

    filterset_fields = ['attribute_id', 'attribute__product_id', ]

    @action(methods=['GET'], detail=False, url_path='all')
    def get_all(self, request):
        return Response(self.serializer_class(self.filter_queryset(self.get_queryset()), many=True).data)
