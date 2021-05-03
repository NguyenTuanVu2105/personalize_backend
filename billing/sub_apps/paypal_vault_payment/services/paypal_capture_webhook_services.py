from billing.sub_apps.paypal_payment.constants.paypal_webhook_resource_type import PaypalWebhookResourceType
from billing.sub_apps.paypal_payment.services.base.paypal_base_webhook_services import PaypalBaseWebhookService
from billing.sub_apps.paypal_vault_payment.services.paypal_order_services import PaypalOrderService


class PaypalCaptureWebhookService(PaypalBaseWebhookService):
    resource_type = PaypalWebhookResourceType.CAPTURE

    @classmethod
    def get_charge_status(cls, transaction_detail):
        return PaypalOrderService.handle_order_transaction_detail(transaction_detail)

    @classmethod
    def get_payment_gateway_invoice_id(cls, webhook_data):
        return cls.get_webhook_resource(webhook_data).get("invoice_id")

    @classmethod
    def rebuild_transaction_data(cls, webhook_data):
        webhook_id = webhook_data.get("id")
        webhook_resource = cls.get_webhook_resource(webhook_data)
        return PaypalOrderService.rebuild_order_transaction_detail(capture_transaction_detail=webhook_resource,
                                                                   webhook_id=webhook_id)
