from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.decorators import action

from HUB.viewsets.base import AuthenticatedGenericViewSet
from support.models import SupportTicketConversation
from support.serializers.ticket_support_serializer import TicketSupportConversationSerializer
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


class TicketConversationViewSet(mixins.RetrieveModelMixin,
                                AuthenticatedGenericViewSet):
    queryset = SupportTicketConversation.objects.all().order_by('-create_time')
    serializer_class = TicketSupportConversationSerializer

    @action(methods=["GET"], detail=False, url_path="by_ticket/(?P<ticket_id>[0-9]{10,})")
    def list_by_ticket(self, request, *args, **kwargs):
        conversations = self.queryset.filter(ticket_id=kwargs["ticket_id"])
        page = self.paginate_queryset(conversations)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(instance=conversations, many=True)
        return Response(serializer.data)
