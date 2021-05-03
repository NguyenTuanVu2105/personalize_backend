import logging

from service_communication.constants.incoming_webhook_statuses import IncomingWebhookStatus
from service_communication.services.incoming_webhook import save_incoming_webhook

logger = logging.getLogger(__name__)


class GenericIncomingWebhookHandle:

    @staticmethod
    def save_webhook(relate_object=None, request_data=None, webhook_type=None, meta=None):
        try:
            return save_incoming_webhook(relate_object, webhook_type, request_data, meta)
        except Exception as e:
            logger.exception(e)
            return None

    def handle_webhook_success(self, incoming_webhook):
        if incoming_webhook is None:
            return
        incoming_webhook.process_description = "success"
        incoming_webhook.status = IncomingWebhookStatus.RESOLVED
        self.handle_webhook_finally(incoming_webhook)

    def handle_webhook_error(self, incoming_webhook, error):
        if incoming_webhook is None:
            return
        if not isinstance(error, str):
            try:
                error = str(error)
            except Exception as e:
                error = str(e)
        incoming_webhook.process_description = error
        incoming_webhook.status = IncomingWebhookStatus.ERROR
        self.handle_webhook_finally(incoming_webhook)

    @staticmethod
    def handle_webhook_finally(incoming_webhook):
        try:
            incoming_webhook.process_count += 1
            incoming_webhook.save(update_fields=['process_count', 'status', 'process_description'])
        except Exception as e:
            logger.exception(e)
