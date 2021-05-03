import datetime
import re

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from HUB.exceptions.FormValidationError import FormValidationError
from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.retrieve_model_mixins import RetrieveWithUserSettingsModelMixin
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixinWithUserSetting
from notification.enums.message_types import MessageType
from notification.models import Template
from notification.services.instant_prompt import remove_instant_ticket_prompt
from order.models import Order
from order.services.service_order import task_update_order_support_ticket_info
from support.constants.ticket_subject_types import TicketSubjectType
from support.constants.ticket_types import SupportTicketType
from support.filter.ticket_filter import TicketFilter
from support.function.check_ticket_order import check_ticket_order_change_size_color, check_ticket_order_change_address
from support.function.parse_order_ids import parse_order_ids
from support.function.scan_tickets_by_time import scan_tickets_by_time
from support.models import SupportTicket, SupportTicketConversation
from support.serializers.ticket_support_serializer import BriefTicketSupportSerializer, \
    TicketSupportConversationSerializer
from support.services.fresh_desk_service import FreshDeskService
from user.queries import RawSearchQuery

User = get_user_model()

import logging

logger = logging.getLogger(__name__)

DELAY_TIME_BETWEEN_TICKET_CREATE_IN_SECONDS = 15


class UserTicketSupportView(CreateModelMixin,
                            SearchableListModelMixinWithUserSetting,
                            RetrieveWithUserSettingsModelMixin,
                            AuthenticatedGenericViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = BriefTicketSupportSerializer
    filterset_class = TicketFilter
    error_messages = {
        "order_ids": {
            "empty": "Order id must be provided",
            "invalid": "Some order is invalid",
            "change_size_color": "Cannot change orders when they have been in production",
            "change_address": "Cannot change address because the orders has been shipped"
        },
        "ticket": {
            "create_time_limit": f"You have just created a ticket recently. Please wait up to {DELAY_TIME_BETWEEN_TICKET_CREATE_IN_SECONDS} seconds to create another ticket"

        }
    }
    """
    Create a model instance.
    """

    def get_queryset(self, q=None):
        if q:
            q = re.sub(r'[!\'()|&<>:*\[\];$\"]', ' ', q).strip()
            q = re.sub(r'\s+', ' & ', q)
            if q.strip():
                q += ':*'
                self.queryset = self.get_queryset().filter(tsv_metadata_search=RawSearchQuery(q))
        return self.queryset.order_by('-create_time').filter(user__id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        ticket = self.get_queryset().get(pk=kwargs['pk'])
        ticket.read = True
        ticket.save()
        remove_instant_ticket_prompt(ticket.user.id)
        return Response(BriefTicketSupportSerializer(ticket).data)

    def create(self, request, *args, **kwargs):
        user_settings = request.user.settings
        if user_settings.last_create_support_ticket_time is not None and (
                timezone.now() - user_settings.last_create_support_ticket_time).total_seconds() < DELAY_TIME_BETWEEN_TICKET_CREATE_IN_SECONDS:
            raise FormValidationError(field="ticket", code="create_time_limit")
        request_data = request.data

        now = datetime.datetime.now()
        formated_now = now.strftime("%H:%M:%S, %b %d %Y")
        order_ids_str = request_data["order_ids"]
        order_ids = request_data["order_ids"].split(",")
        if len(order_ids_str) == 0 or len(order_ids) == 0:
            raise FormValidationError(field="order_ids", code="empty")

        seller_name = request.user.name
        seller_email = request.user.email
        subject = request_data["subject"]
        issue = request_data["issue"]
        type = request_data["type"]

        orders = Order.objects.filter_by_user_id(self.request.user.pk).filter(id__in=order_ids).all()
        number_order = len(orders)
        if len(order_ids) != number_order:
            raise FormValidationError(field="order_ids", code="invalid")

        # change size color
        if type == TicketSubjectType.CHANGE_SIZE_COLOR:
            order_change = check_ticket_order_change_size_color(orders)
            if len(order_change) >= number_order:
                raise FormValidationError(field="order_ids", code="change_size_color")
            elif len(order_change) > 0:
                return Response({"success": False, "warning": True, "order_failed": order_change,
                                 "message": "Order {} can't change size/color because they are producted.".format(
                                     parse_order_ids(order_change))}, status=HTTP_400_BAD_REQUEST)

        elif type == TicketSubjectType.CHANGE_ADDRESS:
            order_change = check_ticket_order_change_address(orders)
            if len(order_change) >= number_order:
                raise FormValidationError(field="order_ids", code="change_address")
            elif len(order_change) > 0:
                return Response({"success": False, "warning": True, "order_failed": order_change,
                                 "message": "Order {} can't change address because they are shipped.".format(
                                     parse_order_ids(order_change))}, status=HTTP_400_BAD_REQUEST)

        admin_template = Template.objects.get(pk=MessageType.SELLER_ORDER_CONTACT_SUPPORT)
        admin_title = admin_template.mail_title.format(order_id=parse_order_ids(order_ids), subject=subject)
        admin_content = admin_template.mail_content.format(time=formated_now, seller=seller_name,
                                                           order_id=parse_order_ids(order_ids),
                                                           content=issue)

        attachments = []
        for file_data in request.FILES.getlist('files'):
            attachments.append((file_data.name, file_data.read()))

        with transaction.atomic():
            ticket = FreshDeskService.create_ticket(subject=admin_title,
                                                    email=seller_email,
                                                    name=seller_name,
                                                    description=admin_content,
                                                    attachments=attachments,
                                                    ticket_type=SupportTicketType.ORDER,
                                                    user=request.user,
                                                    objects=orders)

            user_settings.last_create_support_ticket_time = timezone.now()
            user_settings.save()

        task_update_order_support_ticket_info.delay(ticket.id)
        return Response({"success": True, "message": "Your issue is forwarded successfully to our support team"})

    @action(methods=["GET"], detail=False, url_path="unread_count")
    def unread_count(self, request, *args, **kwargs):
        count = self.get_queryset().filter(read=False).count()
        return Response({"count": count})


    @action(methods=["GET"], detail=False, url_path="by_order/(?P<order_id>[0-9]{10,})")
    def list_by_orders(self, request, *args, **kwargs):
        # Search ticket
        q = request.query_params.get("q")
        ticket_queryset = self.get_queryset(q).filter(targets__object_id=kwargs["order_id"])
        tickets = self.filter_queryset(ticket_queryset)
        page = self.paginate_queryset(tickets)
        serializer = BriefTicketSupportSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=["POST"], detail=True, url_path="reply")
    def create_reply(self, request, *args, **kwargs):
        ticket = self.queryset.get(pk=kwargs['pk'])
        request_data = request.data
        body = request_data['body']

        attachments = []
        for file_data in request.FILES.getlist('files'):
            attachments.append((file_data.name, file_data.read()))

        conversation = FreshDeskService.create_reply(ticket.ticket_id, body, attachments)
        conversation_obj = SupportTicketConversation.objects.create(ticket=ticket, meta=conversation,
                                                                    conversation_id=conversation['id'],
                                                                    create_time=conversation['created_at'],
                                                                    customer_send=True)
        ticket.customer_last_reply = True
        ticket.save()
        return Response({"success": True, "data": TicketSupportConversationSerializer(conversation_obj).data})

    @action(methods=["GET"], detail=False, url_path="test-scan")
    def test(self, request, *args, **kwargs):
        scan_tickets_by_time()
        return Response('rew')
