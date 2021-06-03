import logging

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet, GenericViewSet
from notification.enums.message_statuses import MessageStatus
from notification.models import Message, InstantPrompt
from notification.serializers.message import MessageSerializer
from notification.services import set_num_unread_msg, get_num_unread_msg
from rest_framework import permissions
logger = logging.getLogger(__name__)


class MessageViewSet(mixins.ListModelMixin,
                     AuthenticatedGenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        instant_prompts = InstantPrompt.objects.filter(owner=request.user.pk, status=MessageStatus.UNREAD)
        res.data['instant_prompts'] = list(map(lambda prompt: prompt.verbose_type, instant_prompts))
        count = self.count_unread_message()
        set_num_unread_msg(request.user, count)
        return res

    @action(methods=["POST"], detail=False, url_path="read_all")
    def read_all_message(self, request):
        self.get_queryset().filter(status=MessageStatus.UNREAD).update(status=MessageStatus.READ)
        return Response({"success": True})

    @action(methods=["POST"], detail=False, url_path="read")
    def read_message(self, request):
        return self.update_status(request.data['id'], MessageStatus.READ)

    @action(methods=["POST"], detail=False, url_path="delete")
    def delete_message(self, request):
        return self.update_status(request.data['id'], MessageStatus.DELETED)

    @action(methods=["GET"], detail=False, url_path="unread_count")
    def count_unread(self, request):
        count = get_num_unread_msg(request.user)
        if count is None:
            count = self.count_unread_message()
            set_num_unread_msg(request.user, count)
        instant_prompts = InstantPrompt.objects.filter(owner=request.user.pk, status=MessageStatus.UNREAD)
        return Response({
            "success": True,
            "count": count,
            "instant_prompts": list(map(lambda prompt: prompt.verbose_type, instant_prompts))
        })

    def update_status(self, message_id, status):
        message = self.get_queryset().get(pk=message_id)
        message.status = status
        message.save()
        set_num_unread_msg(self.request.user, self.count_unread_message())
        return Response({"success": True})

    def count_unread_message(self):
        return self.queryset.filter(owner=self.request.user.pk, status=MessageStatus.UNREAD).exclude(
            content__contains="<a").count()
