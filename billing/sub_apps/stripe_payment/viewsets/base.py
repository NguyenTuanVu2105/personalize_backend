from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class AuthenticatedModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
