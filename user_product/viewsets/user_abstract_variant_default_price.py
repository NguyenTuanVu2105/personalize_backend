from rest_framework import mixins
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from ..models import UserAbstractVariantDefaultPrice
from ..serializers import UserAbstractVariantDefaultPriceSerializer


class UserAbstractVariantDefaultPriceViewSet(mixins.ListModelMixin,
                                             AuthenticatedGenericViewSet):
    queryset = UserAbstractVariantDefaultPrice.objects.all().order_by('-update_time')
    serializer_class = UserAbstractVariantDefaultPriceSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id', None)
        if product_id is None:
            return Response({"success": False, "message": "product_id is none"})
        default_prices = self.get_queryset().filter(abstract_variant__product__id=product_id)
        return Response(UserAbstractVariantDefaultPriceSerializer(default_prices, many=True).data)
