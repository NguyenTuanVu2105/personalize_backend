from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from user.models import UserTag
from user.serializers import UserTagSerializer


class UserTagViewSet(AdminGenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = UserTag.objects.all()
    serializer_class = UserTagSerializer
    filterset_fields = ['user']

    def list(self, request, *args, **kwargs):
        return super(UserTagViewSet, self).list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='all-available-tags')
    def get_all_available_tags(self, request):
        available_tags = self.queryset.values_list('tag', flat=True).distinct().order_by()
        return Response({'tags': available_tags})

    def create(self, request, *args, **kwargs):
        request_data = request.data
        user_id = request_data.get('user_id')
        tag = ' '.join(request_data.get('tag').split())
        user_tag, created = UserTag.objects.get_or_create(user_id=user_id, tag=tag)
        if created:
            data = self.get_serializer(user_tag).data
            return Response({'success': True, 'data': data})
        else:
            return Response({'success': False, 'message': 'Tag is already existed'})
