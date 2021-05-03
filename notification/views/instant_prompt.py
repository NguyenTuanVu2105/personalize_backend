import logging
import traceback

from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.permissions import get_permissions
from HUB.viewsets.base import AuthenticatedGenericViewSet
from notification.enums.instant_prompt_types import INSTANT_PROMPT_TYPE_VERBOSE_DICT, INSTANT_PROMPT_TYPE_DICT
from notification.enums.message_statuses import MessageStatus
from notification.functions import renew_instant_prompt
from notification.models import InstantPrompt

logger = logging.getLogger(__name__)

User = get_user_model()


class InstantPromptViewSet(AuthenticatedGenericViewSet):
    queryset = InstantPrompt.objects.all()
    serializer_class = InstantPrompt

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.pk)

    @action(methods=["POST"], detail=False, url_path="ignore")
    def ignore(self, request):
        prompt_type = request.data['type']
        if prompt_type in INSTANT_PROMPT_TYPE_VERBOSE_DICT:
            self.get_queryset().filter(status=MessageStatus.UNREAD,
                                       type=INSTANT_PROMPT_TYPE_VERBOSE_DICT[prompt_type]).update(
                status=MessageStatus.READ)
            instant_prompts = InstantPrompt.objects.filter(owner=request.user.pk, status=MessageStatus.UNREAD)
            return Response({
                "success": True,
                "instant_prompts": list(map(lambda prompt: prompt.verbose_type, instant_prompts))
            })
        else:
            return Response({
                "success": False
            })

    @action(methods=["GET"], detail=False, url_path="list",
            permission_classes=get_permissions(['admin_instant_prompt_view']))
    def list_instant_prompt(self, request):
        return Response({"success": True, "data": INSTANT_PROMPT_TYPE_DICT})

    @action(methods=["POST"], detail=False, url_path="renew",
            permission_classes=get_permissions(['admin_instant_prompt_update']))
    def renew_instant_prompt(self, request):
        try:
            request_data = request.data
            instant_id = request_data["ipId"]
            renew_instant_prompt(instant_id)
            return Response({"success": True})

        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.info(str(e))
            return Response({"success": False})
