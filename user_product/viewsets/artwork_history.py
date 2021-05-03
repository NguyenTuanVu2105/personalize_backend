from rest_framework import mixins

from HUB.viewsets.base import AuthenticatedGenericViewSet
from user_product.models import ArtworkHistory
from ..serializers import ArtworkHistorySerializer


class ArtworkHistoryViewSet(mixins.ListModelMixin,
                            AuthenticatedGenericViewSet):
    queryset = ArtworkHistory.objects.all().order_by('-create_time')
    serializer_class = ArtworkHistorySerializer

    def get_queryset(self):
        original = self.request.query_params.get('original', None)
        return self.queryset.filter(original_artwork__owner=self.request.user.id, original_artwork=original).order_by('-create_time')
