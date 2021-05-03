from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView as OriginalAPIView

from HUB.viewsets.mixins.base import BaseMixin


class APIView(BaseMixin, OriginalAPIView):
    permission_classes = ()


class AuthenticatedAPIView(APIView):
    permission_classes = (IsAuthenticated,)


class AdminAPIView(APIView):
    permission_classes = (IsAdminUser,)
