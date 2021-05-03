from rest_framework import mixins
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from user_product.models import UploadedMockup
from user_product.serializers import UploadedMockupSerializer


class UploadedMockupViewSet(mixins.CreateModelMixin, AuthenticatedGenericViewSet):
    queryset = UploadedMockup.objects.all()
    serializer_class = UploadedMockupSerializer

    def get_queryset(self):
        return self.queryset

    def create(self, request, *args, **kwargs):
        request_data = request.data
        owner = request.user
        for mockup_url in request_data['mockups_url']:
            UploadedMockup.objects.create(owner=owner, file_url=mockup_url)
        return Response({"success": True})