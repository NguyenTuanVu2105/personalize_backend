from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from order.models.sample_shipping_address import SampleShippingAddress
from order.serializers import SampleShippingAddressSerializer


class UserShippingAddressViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin,
                                 CreateModelMixin, AuthenticatedGenericViewSet):
    queryset = SampleShippingAddress.objects.all()
    serializer_class = SampleShippingAddressSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super().create(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='all')
    def get_all(self, request):
        return Response(self.serializer_class(self.get_queryset(), many=True).data)
