from billing.exceptions.invoice_exception import InvoiceDoesNotExist
from billing.exceptions.webhook_exception import InvalidWebhookResourceType
from billing.models import Invoice
from billing.sub_apps.combine_payment.functions.check_transaction_pending_charge import TransactionPendingChecker
from billing.sub_apps.paypal_payment.constants.paypal_webhook_resource_type import PaypalWebhookResourceType


class PaypalBaseWebhookService:
    resource_type = PaypalWebhookResourceType.UNKNOWN

    @classmethod
    def handle_webhook_data(cls, webhook_data):
        paypal_resource_type = webhook_data.get("resource_type")
        if paypal_resource_type != cls.resource_type:
            raise InvalidWebhookResourceType(
                "Invalid paypal webhook's resource_type {} sent to app".format(cls.resource_type))
        payment_gateway_invoice_id = cls.get_payment_gateway_invoice_id(webhook_data)
        transaction_detail = cls.rebuild_transaction_data(webhook_data)
        charge_status = cls.get_charge_status(transaction_detail)
        transaction_obj = cls.process_charge_result(payment_gateway_invoice_id, charge_status, transaction_detail)
        return transaction_obj

    @classmethod
    def process_charge_result(cls, payment_gateway_invoice_id, charge_status, transaction_detail):
        invoice_obj = Invoice.objects.transaction_pending().get_by_payment_gateway_invoice_id(
            payment_gateway_invoice_id)
        if not invoice_obj:
            raise InvoiceDoesNotExist(
                "Invalid paypal webhook's invoice_id {} sent to app".format(payment_gateway_invoice_id))

        # ignoring update transaction data from paypal webhook
        # in case this transaction was checked completion status by scheduler
        pending_transaction_obj = invoice_obj.transactions.pending().first()
        if not pending_transaction_obj:
            return None
        TransactionPendingChecker.handle_pending_charge_after_check(invoice_obj, pending_transaction_obj, charge_status,
                                                                    transaction_detail)
        return pending_transaction_obj

    @classmethod
    def get_charge_status(cls, transaction_detail):
        raise NotImplementedError("method get_charge_status is not implemented")

    @classmethod
    def get_payment_gateway_invoice_id(cls, webhook_data):
        raise NotImplementedError("method get_payment_gateway_invoice_id is not implemented")

    @classmethod
    def get_webhook_resource(cls, webhook_data):
        return webhook_data.get("resource")

    @classmethod
    def rebuild_transaction_data(cls, webhook_data):
        raise NotImplementedError("method rebuild_transaction_data is not implemented")
