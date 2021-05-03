import logging

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from HUB.viewsets.base import AuthenticatedGenericViewSet
from order.forms.order_comments import OrderCommentsForm
from order.models import OrderComments
from order.serializers.order_comments import OrderCommentsSerializer

logger = logging.getLogger(__name__)


class OrderCommentsViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin,
                           CreateModelMixin, AuthenticatedGenericViewSet):
    queryset = OrderComments.objects.all()
    serializer_class = OrderCommentsSerializer
    filterset_fields = ['order_id', ]

    def get_queryset(self):
        return self.queryset.order_by('create_time')

    def create(self, request, *args, **kwargs):
        try:
            request_data = request.data
            order_comment_check = OrderCommentsForm(data=request_data)
            if order_comment_check.is_valid():
                author = request.user
                content = request.data.get('content', None)
                order = request.data.get('order', None)
                OrderComments.objects.create(author=author, content=content, order_id=order)
                return Response(status=200, data={"success"})
            else:
                return Response(status=400, data=order_comment_check.errors.get_json_data())
        except Exception as e:
            return Response(status=400, data={'status': 'error', 'message': "except"})

    @action(methods=['GET'], detail=False, url_path='all')
    def get_all(self, request):
        return Response(self.serializer_class(self.filter_queryset(self.get_queryset()), many=True).data)
