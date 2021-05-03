from datetime import timedelta

from django.utils import timezone

from order.services import update_order_pack_tracking
from order.services.service_order import process_order, reject_order
from service_communication.constants.incoming_webhook_statuses import IncomingWebhookStatus
from service_communication.constants.incoming_webhook_types import IncomingWebhookType
from service_communication.models.incoming_webhook_log import IncomingWebhook

CHECK_PENDING_WEBHOOK_IN_MINUTE = 5


def save_incoming_webhook(relate_object, webhook_type, body_data, meta, status=IncomingWebhookStatus.PENDING):
    return IncomingWebhook.objects.create(relate_object=relate_object,
                                          type=webhook_type,
                                          body_data=body_data,
                                          status=status,
                                          meta=meta)


ALLOW_CANCELED_WEBHOOK_STATUSES = [IncomingWebhookStatus.PENDING, IncomingWebhookStatus.ERROR]


def cancel_incoming_webhook(user, incoming_webhook, request_data):
    if incoming_webhook.status not in ALLOW_CANCELED_WEBHOOK_STATUSES:
        return
    incoming_webhook.process_description = f"User {user.id} canceled"
    incoming_webhook.status = IncomingWebhookStatus.CANCELLED
    incoming_webhook.save(update_fields=['process_description', 'status'])


def auto_process_pending_incoming_webhooks():
    due_time = timezone.now() - timedelta(minutes=CHECK_PENDING_WEBHOOK_IN_MINUTE)
    pending_webhooks = IncomingWebhook.objects.filter(status=IncomingWebhookStatus.PENDING,
                                                      update_time__lt=due_time)[:10]
    for pending_webhook in pending_webhooks:
        process_incoming_webhook(pending_webhook)


def process_incoming_webhook(webhook):
    webhook.process_count += 1
    try:
        webhook_type = webhook.type
        if webhook_type == IncomingWebhookType.FULFILL_PROCESS_ORDER:
            process_order(webhook.relate_object, webhook.body_data)
        elif webhook_type == IncomingWebhookType.FULFILL_REJECT_ORDER:
            reject_order(webhook.relate_object, webhook.body_data)
        elif webhook_type == IncomingWebhookType.FULFILL_UPDATE_TRACKING:
            update_order_pack_tracking(webhook.relate_object, webhook.body_data)
        else:
            webhook.process_description = "Cannot find handler for " + webhook_type
            webhook.status = IncomingWebhookStatus.CANCELLED
            webhook.save(update_fields=['process_description', 'status', 'process_count'])
            return
        webhook.process_description = "success"
        webhook.status = IncomingWebhookStatus.RESOLVED
    except Exception as e:
        webhook.process_description = str(e)
        webhook.status = IncomingWebhookStatus.ERROR
    finally:
        webhook.save(update_fields=['process_description', 'status', 'process_count'])
