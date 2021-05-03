import json
import logging

from freshdesk.v2.api import TicketAPI, API, CommentAPI, AgentAPI
from freshdesk.v2.models import Ticket, Comment, Agent

logger = logging.getLogger(__name__)
DEFAULT_CONVERSATION_PER_PAGE = 30


class FreshDeskAgentAPI(AgentAPI):
    def create_agent(self, email, ticket_scope, **kwargs):
        url = "agents"
        data = {'ticket_scope': ticket_scope, 'email': email}
        data.update(kwargs)
        response = self._api._post(url, data=json.dumps(data))
        return Agent(**response)


class FreshDeskConversationAPI(CommentAPI):
    def list_conversations(self, ticket_id):
        result = []
        page = 1
        while True:
            url = 'tickets/{}/conversations?page={}'.format(ticket_id, page)
            res = self._api._get(url)
            result.extend(res)
            if len(res) < DEFAULT_CONVERSATION_PER_PAGE:
                break
            page += 1
        return result

    def create_reply(self, ticket_id, body, **kwargs):
        url = 'tickets/%d/notes' % ticket_id
        data = {'body': body}
        data.update(kwargs)
        if 'attachments' in data and len(data['attachments']) > 0:
            response = self.create_reply_with_attachment(ticket_id, data)
            return response
        else:
            data.pop('attachments')
        response = self._api._post(url, data=json.dumps(data))
        return response

    def create_reply_with_attachment(self, ticket_id, data, **kwargs):
        url = 'tickets/%d/notes' % ticket_id
        attachments = data.pop('attachments')
        multipart_data = []

        for attachment in attachments:
            multipart_data.append(('attachments[]', (attachment[0], attachment[1], None)))

        for key, value in data.copy().items():
            # Reformat ticket properties to work with the multipart/form-data encoding.
            if isinstance(value, list) and not key.endswith('[]'):
                data[key + '[]'] = value
                del data[key]
        logger.info(data)
        response = self._api._post(url, data=data, files=multipart_data, headers={'Content-Type': None})
        return response


class FreshDeskTicketAPI(TicketAPI):
    def get_ticket_with_conversation(self, ticket_id):
        url = 'tickets/%d?include=conversations' % ticket_id
        ticket = self._api._get(url)
        return ticket

    def list_ticket_updated_since(self, updated_since, ticket_per_page):
        url = 'tickets?updated_since={}&order_by=updated_at&order_type=asc&per_page={}'.format(updated_since,
                                                                                               ticket_per_page)
        tickets = self._api._get(url)
        return [Ticket(**t) for t in tickets]

    def create_ticket(self, subject, **kwargs):
        """
            Creates a ticket
            To create ticket with attachments,
            pass a key 'attachments' with value as list of fully qualified file paths in string format.
            ex: attachments = ('/path/to/attachment1', '/path/to/attachment2')
        """

        url = 'tickets'
        status = kwargs.get('status', 2)
        priority = kwargs.get('priority', 1)
        data = {
            'subject': subject,
            'status': status,
            'priority': priority,
        }
        data.update(kwargs)
        if 'attachments' in data and len(data['attachments']) > 0:
            ticket = self._create_ticket_with_attachment(url, data)
            logger.info(ticket)
            return Ticket(**ticket)
        else:
            data.pop('attachments')
        ticket = self._api._post(url, data=json.dumps(data))
        return Ticket(**ticket)

    def _create_ticket_with_attachment(self, url, data):
        attachments = data.pop('attachments')
        multipart_data = []

        for attachment in attachments:
            multipart_data.append(('attachments[]', (attachment[0], attachment[1], None)))

        for key, value in data.copy().items():
            # Reformat ticket properties to work with the multipart/form-data encoding.
            if isinstance(value, list) and not key.endswith('[]'):
                data[key + '[]'] = value
                del data[key]

        if 'custom_fields' in data and isinstance(data['custom_fields'], dict):
            # Reformat custom fields to work with the multipart/form-data encoding.
            for field, value in data['custom_fields'].items():
                data['custom_fields[{}]'.format(field)] = value
            del data['custom_fields']

        # Override the content type so that `requests` correctly sets it to multipart/form-data instead of JSON.
        return self._api._post(url, data=data, files=multipart_data, headers={'Content-Type': None})


class FreshDeskAPI(API):
    def __init__(self, **kwargs):
        super(FreshDeskAPI, self).__init__(**kwargs)
        self.tickets = FreshDeskTicketAPI(self)
        self.conversations = FreshDeskConversationAPI(self)
        self.agents = FreshDeskAgentAPI(self)
