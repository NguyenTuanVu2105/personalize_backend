from billing.sub_apps.paypal_payment.constants.paypal_webhook_resource_type import PaypalWebhookResourceType
from billing.sub_apps.paypal_payment.services.base.paypal_base_webhook_services import PaypalBaseWebhookService
from billing.sub_apps.paypal_payment.services.paypal_sale_services import PaypalSaleService


class PaypalSaleWebhookService(PaypalBaseWebhookService):
    resource_type = PaypalWebhookResourceType.SALE

    @classmethod
    def get_charge_status(cls, transaction_detail):
        return PaypalSaleService.handle_payment_transaction_detail(transaction_detail)

    @classmethod
    def get_payment_gateway_invoice_id(cls, webhook_data):
        return cls.get_webhook_resource(webhook_data).get("invoice_number")

    @classmethod
    def rebuild_transaction_data(cls, webhook_data):
        webhook_id = webhook_data.get("id")
        webhook_resource = cls.get_webhook_resource(webhook_data)
        return PaypalSaleService.rebuild_payment_transaction_detail(sale_transaction_detail=webhook_resource,
                                                                    webhook_id=webhook_id)
