from HUB.constants.celery_task import CeleryTask
from support.services.fresh_desk_service import FreshDeskService
import logging
from helper.leader_election import is_master
from celery.decorators import task

from ..models import SupportTicket

logger = logging.getLogger(__name__)


@task(name=CeleryTask.TASK_UPDATE_TICKET_CONVERSATION)
def task_update_ticket_conversation(ticket_id):
    try:
        FreshDeskService.update_conversations(ticket_id)
    except Exception as e:
        ticket = SupportTicket.objects.filter(ticket_id=ticket_id).first()
        logger.info("Ticket error {}".format(ticket_id))
        ticket.need_update = True
        ticket.save()
        logger.error(e)

def scan_tickets_by_time():
    ticket_ids = FreshDeskService.list_ticket_updated_since()
    for ticket_id in ticket_ids:
        task_update_ticket_conversation.delay(ticket_id)
    # task_update_ticket_conversation.delay(12)
