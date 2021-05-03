import logging

from rest_framework.response import Response

from HUB.permissions.permissions import HeaderBaseAuthentication
from HUB.viewsets.base import BaseGenericAPIView
from notification.enums.message_types import MessageType
from notification.services import send_notification_task
from order.services.service_order import task_update_order_support_ticket_info
from service_communication.constants.authenticated_service import AuthenticatedService
from support.constants.ticket_statuses import SUPPORT_TICKET_STATUS_VERBOSE_DICT, SupportTicketStatus
from support.constants.ticket_types import SupportTicketType
from support.models import SupportTicket
from rest_framework.decorators import action

logger = logging.getLogger(__name__)


class TicketUpdateHookView(BaseGenericAPIView):
    permission_classes = [HeaderBaseAuthentication]
    service_name = AuthenticatedService.FRESH_DESK_WEBHOOK

    def post(self, request):
        # logger.info(request.data)
        webhook_data = request.data['freshdesk_webhook']
        ticket_status = webhook_data['ticket_status'].lower()
        ticket = SupportTicket.objects.get(ticket_id=webhook_data['ticket_id'])
        if ticket is not None:
            status = SUPPORT_TICKET_STATUS_VERBOSE_DICT[ticket_status]
            ticket.status = status
            if status in [SupportTicketStatus.RESOLVED, SupportTicketStatus.CLOSED]:
                ticket.customer_last_reply = None
                ticket.save()
                send_notification_task.delay(ticket.user.id, MessageType.TICKET_RESOLVED, {"ticket_id": ticket.id})
            if ticket.type == SupportTicketType.ORDER:
                task_update_order_support_ticket_info.delay(ticket.id)

        return Response({"success": True, "message": ""})
