import logging

from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from ..serializers import UserSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class UserViewSet(mixins.RetrieveModelMixin,
                  AuthenticatedGenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(pk=self.request.user.pk)

    @action(methods=["POST"], detail=False, url_path='log')
    def log(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user
        message = request_data.get('message')
        logger.info(f"User: ({user.id}, {user.email}, {user.is_test_user}) | Message: {message}")
        return Response({})
