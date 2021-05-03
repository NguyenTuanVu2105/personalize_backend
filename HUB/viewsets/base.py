from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet as BaseGenericViewSet

from HUB import logger
from HUB.helpers.auth_helper import get_refresh_token_val
from HUB.permissions import IsAuthenticated
from HUB.settings import ACCESS_TOKEN_HEADER
from rest_framework_jwt.settings import api_settings
from HUB.viewsets.mixins.base import BaseMixin



class GenericViewSet(BaseGenericViewSet):
    ordering_fields = []


class GenericAPIView(APIView):
    pass


class GenericAuthViewSet(BaseGenericViewSet):
    ordering_fields = []


class AuthenticatedGenericViewSet(BaseMixin, GenericAuthViewSet):
    permission_classes = [IsAuthenticated]


class AdminGenericViewSet(BaseMixin, GenericAuthViewSet):
    permission_classes = [IsAdminUser]
    # pass


class AdminGenericAPIView(BaseMixin, GenericAPIView):
    permission_classes = [IsAdminUser]


class BaseGenericAPIView(BaseMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
