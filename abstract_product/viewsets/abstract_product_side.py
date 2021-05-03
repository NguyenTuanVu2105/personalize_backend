from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from abstract_product.models import AbstractProductSide
from abstract_product.serializers.abstract_product_side import AbstractProductSideSerializer


class AbstractProductSideViewSet(ListModelMixin, RetrieveModelMixin, AdminGenericViewSet):
    queryset = AbstractProductSide.objects.all()
    serializer_class = AbstractProductSideSerializer
    filterset_fields = ['abstract_product_id', ]

    @action(methods=['GET'], detail=False, url_path='all')
    def get_all(self, request, *args, **kwargs):
        return Response({'success': True, 'data': self.get_serializer(
            self.filter_queryset(self.get_queryset()), many=True
        ).data})
