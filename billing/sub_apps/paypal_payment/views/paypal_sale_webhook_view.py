from billing.sub_apps.paypal_payment.services.paypal_sale_webhook_services import PaypalSaleWebhookService
from billing.sub_apps.paypal_payment.views.base.paypal_webhook_view import PaypalWebhookView
from service_communication.constants.incoming_webhook_types import IncomingWebhookType


class PaypalSaleWebhookView(PaypalWebhookView):
    paypal_webhook_service = PaypalSaleWebhookService
    webhook_type = IncomingWebhookType.PAYPAL_SALE_TRANSACTION_UPDATE
