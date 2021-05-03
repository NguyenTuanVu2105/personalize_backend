import logging
from datetime import timedelta

from django.utils import timezone

from HUB import settings
from HUB.settings import FRESH_DESK_DOMAIN, TICKET_PER_MINUTE, \
    SUPPORT_AGENT_ID, TICKET_UPDATE_LIMIT
from helper.list_helpers import remove_duplicate
from notification.enums.instant_prompt_types import InstantPromptType
from notification.enums.message_types import MessageType
from notification.services import send_notification_task
from notification.services.instant_prompt import create_instant_prompt, remove_instant_ticket_prompt
from service_communication.constants.schedule_type import ScheduleType
from service_communication.models import ScheduleInfo
from support.constants.ticket_statuses import SUPPORT_TICKET_STATUS_VERBOSE_DICT, SupportTicketStatus
from support.function.is_customer_send import is_customer_send
from support.models import SupportTicket, SupportTicketTarget, SupportTicketConversation
from support.services.fresh_desk_sdk import FreshDeskAPI

logger = logging.getLogger(__name__)
DEFAULT_UPDATED_SINCE = '2000-07-15'


class FreshDeskService:
    FreshDeskApi = FreshDeskAPI(domain=settings.FRESH_DESK_DOMAIN, api_key=settings.FRESH_DESK_API_KEY)

    @classmethod
    def create_ticket(cls, objects, ticket_type, user, **kwargs):
        ticket = cls.FreshDeskApi.tickets.create_ticket(**kwargs)
        support_ticket, created = SupportTicket.objects.update_or_create(
            ticket_id=ticket.id,
            defaults={
                "user": user,
                "type": ticket_type,
                "status": SUPPORT_TICKET_STATUS_VERBOSE_DICT.get(
                    ticket.status,
                    SupportTicketStatus.OPEN),
                "subject": ticket.subject,
                "attachments": ticket.attachments,
                "update_time": timezone.now(),
                "description": ticket.description,
                "url": "https://{}/helpdesk/tickets/{}".format(FRESH_DESK_DOMAIN, ticket.id)
            })
        SupportTicketTarget.objects.bulk_create(
            list(map(lambda o: SupportTicketTarget(content_object=o, ticket=support_ticket), objects)))
        return support_ticket

    @classmethod
    def update_conversations(cls, ticket_id, **kwargs):
        ticket = SupportTicket.objects.filter(ticket_id=ticket_id).first()
        if not ticket:
            return
        logger.info("Update ticket {}".format(ticket.ticket_id))
        conversations_res = cls.FreshDeskApi.conversations.list_conversations(ticket_id)
        conversation_create = []
        for conversation in conversations_res:
            if not SupportTicketConversation.objects.filter(conversation_id=conversation['id']).exists():
                conversation_create.append(conversation)
        if len(conversation_create) > 0:
            logger.info("Add {} conversations".format(len(conversation_create)))
            SupportTicketConversation.objects.bulk_create(
                list(map(lambda conv: SupportTicketConversation(conversation_id=conv['id'], ticket=ticket, meta=conv,
                                                                create_time=conv['created_at'],
                                                                customer_send=is_customer_send(conv)),
                         conversation_create)))
            if not is_customer_send(conversation_create[-1]):
                ticket.read = False
                ticket.customer_last_reply = False
                ticket.save()
                create_instant_prompt(ticket.user.id, InstantPromptType.TICKET_UNREAD)
            else:
                ticket.read = True
                ticket.customer_last_reply = True
                ticket.save()
                remove_instant_ticket_prompt(ticket.user.id)

    @classmethod
    def list_ticket_updated_since(cls):
        ticket_ids = []

        # Update List Ticket Error
        tickets_need_update = SupportTicket.objects.filter(need_update=True)
        ticket_need_update_ids = [x.ticket_id for x in tickets_need_update]
        tickets_need_update.update(need_update=False)
        ticket_ids.extend(ticket_need_update_ids)
        logger.info("Ticket error: {}".format(ticket_need_update_ids))

        # Update ticket by time
        while True:
            # get update time
            ticket_scan_info = ScheduleInfo.objects.filter(schedule_type=ScheduleType.AUTO_SCAN_SUPPORT_TICKET)
            updated_since = ticket_scan_info[0].meta['updated_at'] if ticket_scan_info else DEFAULT_UPDATED_SINCE
            logger.info("Scan tickets start {}".format(updated_since))

            # Call freshdesk service
            tickets_from_service = cls.FreshDeskApi.tickets.list_ticket_updated_since(updated_since,
                                                                                      TICKET_PER_MINUTE)

            # Update ticket
            for ticket in tickets_from_service:
                ticket_obj = SupportTicket.objects.filter(ticket_id=ticket.id).first()
                status = SUPPORT_TICKET_STATUS_VERBOSE_DICT[ticket.status]
                if ticket_obj:
                    if not ticket_obj.update_time == ticket.updated_at:
                        ticket_obj.update_time = ticket.updated_at
                        if not ticket_obj.is_resolved and status in [SupportTicketStatus.CLOSED,
                                                                       SupportTicketStatus.RESOLVED]:
                            ticket_obj.status = status
                            ticket_obj.customer_last_reply = None
                            send_notification_task.delay(ticket_obj.user.id, MessageType.TICKET_RESOLVED,
                                                         {"ticket_id": ticket_obj.id})
                        ticket_obj.save()

                        ticket_ids.append(ticket_obj.ticket_id)
            last_update = tickets_from_service[-1].updated_at
            ScheduleInfo.objects.update_or_create(schedule_type=ScheduleType.AUTO_SCAN_SUPPORT_TICKET,
                                                  defaults={
                                                      "meta": {
                                                          "updated_at": last_update.strftime("%Y-%m-%dT%H:%M:%SZ")
                                                      }
                                                  })

            if len(ticket_ids) >= TICKET_UPDATE_LIMIT or len(tickets_from_service) < TICKET_PER_MINUTE:
                break
        ticket_ids = remove_duplicate(ticket_ids)
        logger.info("Scan ticket: {}".format(ticket_ids))
        logger.info("Scan tickets end {}".format(last_update))
        return ticket_ids

    @classmethod
    def create_reply(cls, ticket_id, body, attachments=None):
        data = {"user_id": SUPPORT_AGENT_ID}
        res = cls.FreshDeskApi.conversations.create_reply(ticket_id=ticket_id, body=body, attachments=attachments,
                                                          **data)
        ticket = SupportTicket.objects.filter(ticket_id=ticket_id).first()
        ticket.updated_at = res['created_at']
        ticket.save()
        return res

    @classmethod
    def create_agent(cls, **kwargs):
        cls.FreshDeskApi.agents.create_agent()
