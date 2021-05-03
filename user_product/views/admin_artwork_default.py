from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from HUB.paginations import EnhancedPageNumberPagination
from HUB.permissions import get_permissions
from HUB.viewsets.base import AdminGenericViewSet
from user_product.models import ArtworkDefault
from user_product.services.artwork_default import upload_artwork_default, \
    delete_artwork_default, update_artwork_default
from user_product.serializers import ArtworkSerializer


class AdminArtworkDefault(ListModelMixin, AdminGenericViewSet):
    queryset = ArtworkDefault.objects.all()
    pagination_class = EnhancedPageNumberPagination
    serializer_class = ArtworkSerializer
    filterset_fields = ['product_side']

    @action(methods=["POST"], detail=False, url_path="upload",
            permission_classes=get_permissions(['admin_artwork_default_modify']))
    def upload(self, request, *args, **kwargs):
        result = upload_artwork_default(request)
        return Response(ArtworkSerializer(result).data)

    @action(methods=["DELETE"], detail=True, url_path="delete",
            permission_classes=get_permissions(['admin_artwork_default_modify']))
    def delete(self, request, *args, **kwargs):
        delete_artwork_default(self.get_object())
        return Response({'success': True})

    @action(methods=["PUT"], detail=True, url_path="update",
            permission_classes=get_permissions(['admin_artwork_default_modify']))
    def put(self, request, *args, **kwargs):
        result = update_artwork_default(self.get_object(), request)
        return Response(ArtworkSerializer(result).data)
