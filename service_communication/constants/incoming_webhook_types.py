class IncomingWebhookType:
    FULFILL_PROCESS_ORDER = "0"
    FULFILL_UPDATE_TRACKING = "1"
    FULFILL_REJECT_ORDER = "2"
    PAYPAL_SALE_TRANSACTION_UPDATE = "3"
    PAYPAL_CAPTURE_TRANSACTION_UPDATE = "4"
    TRACKING_TOOL_UPDATE_TRACKER = "5"


class VerboseIncomingWebhookType:
    FULFILL_PROCESS_ORDER = "fulfill_process_order"
    FULFILL_UPDATE_TRACKING = "fulfill_update_tracking"
    FULFILL_REJECT_ORDER = "fulfill_reject_order"
    PAYPAL_SALE_TRANSACTION_UPDATE = "paypal_sale_transaction_update"
    PAYPAL_CAPTURE_TRANSACTION_UPDATE = "paypal_capture_transaction_update"
    TRACKING_TOOL_UPDATE_TRACKER = "tracking_tool_update_tracker"

INCOMING_WEBHOOK_TYPE_CHOICES = [
    (IncomingWebhookType.FULFILL_PROCESS_ORDER, VerboseIncomingWebhookType.FULFILL_PROCESS_ORDER),
    (IncomingWebhookType.FULFILL_UPDATE_TRACKING, VerboseIncomingWebhookType.FULFILL_UPDATE_TRACKING),
    (IncomingWebhookType.FULFILL_REJECT_ORDER, VerboseIncomingWebhookType.FULFILL_REJECT_ORDER),
    (IncomingWebhookType.PAYPAL_SALE_TRANSACTION_UPDATE, VerboseIncomingWebhookType.PAYPAL_SALE_TRANSACTION_UPDATE),
    (IncomingWebhookType.PAYPAL_CAPTURE_TRANSACTION_UPDATE, VerboseIncomingWebhookType.PAYPAL_CAPTURE_TRANSACTION_UPDATE),
    (IncomingWebhookType.TRACKING_TOOL_UPDATE_TRACKER, VerboseIncomingWebhookType.TRACKING_TOOL_UPDATE_TRACKER)
]
