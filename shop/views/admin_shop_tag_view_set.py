from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from shop.models import ShopTag
from shop.serializers import ShopTagSerializer


class AdminShopTagViewSet(AdminGenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = ShopTag.objects.all()
    serializer_class = ShopTagSerializer
    filterset_fields = ['shop']

    def list(self, request, *args, **kwargs):
        return super(AdminShopTagViewSet, self).list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='all-available-tags')
    def get_all_available_tags(self, request):
        available_tags = self.queryset.values_list('tag', flat=True).distinct().order_by()
        return Response({'tags': available_tags})

    def create(self, request, *args, **kwargs):
        request_data = request.data
        shop_id = request_data.get('shop_id')
        tag = ' '.join(request_data.get('tag').split())
        shop_tag, created = ShopTag.objects.get_or_create(shop_id=shop_id, tag=tag)
        if created:
            data = self.get_serializer(shop_tag).data
            return Response({'success': True, 'data': data})
        else:
            return Response({'success': False, 'message': 'Tag is already existed'})
