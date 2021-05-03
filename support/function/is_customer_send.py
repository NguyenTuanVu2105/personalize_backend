import logging

from HUB.settings import SUPPORT_AGENT_ID

logger = logging.getLogger(__name__)


def is_customer_send(conversation_dict):
    incoming = conversation_dict['incoming'] if "incoming" in conversation_dict else False
    agent_id = conversation_dict['user_id'] == SUPPORT_AGENT_ID if "user_id" in conversation_dict else False
    return incoming or agent_id


