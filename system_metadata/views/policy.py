import logging
import traceback

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AuthenticatedGenericViewSet
from helper.string_helpers import remove_unsafe_html_elements
from system_metadata.forms.policy import PolicyForm
from system_metadata.models import Policy
from system_metadata.serializers import PolicySerializer, BriefPolicySerializer

logger = logging.getLogger(__name__)


class PolicyViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    AuthenticatedGenericViewSet):
    serializer_class = PolicySerializer
    queryset = Policy.objects.all()

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    @action(methods=["GET"], detail=False, url_path="list-prompt")
    def list_prompt(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_prompt=True)
        return Response(PolicySerializer(queryset, many=True).data)
