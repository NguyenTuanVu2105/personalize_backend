from django.db.models import Q
from rest_framework import mixins
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from user_product.models import UserFontFamily
from ..serializers import UserFontFamilySerializer


class UserFontFamilyViewSet(mixins.ListModelMixin,
                            AuthenticatedGenericViewSet):
    queryset = UserFontFamily.objects.all().order_by('title')
    serializer_class = UserFontFamilySerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True).filter(Q(owner=self.request.user.id) | Q(owner=None))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserFontFamilySerializer(instance=queryset, many=True)
        return Response(serializer.data)
