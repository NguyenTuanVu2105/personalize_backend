import logging

from HUB.forms.base import ModelForm
from billing.models import Transaction
from billing.sub_apps.combine_payment.constants import PaymentGateway
from billing.sub_apps.payoneer_payment.services.payoneer_auto_charge import payoneer_get_transaction_id
from billing.sub_apps.paypal_payment.services.paypal_sale_services import PaypalSaleService
from billing.sub_apps.paypal_vault_payment.services.paypal_order_services import PaypalOrderService

logging.basicConfig()
logger = logging.getLogger(__name__)


class TransactionCreationForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "type", "payment_method", "payment_gateway", "status", "detail", "idempotency_key",
                  "payment_gateway_transaction_id"]
        optional_fields = ["status", "amount", "payment_gateway", "payment_method", "idempotency_key",
                           "payment_gateway_transaction_id"]

    def clean_amount(self):
        return self.data.get("content_object").amount

    def update_payment_gateway_transaction_id(self, cleaned_data):
        payment_gateway = cleaned_data.get("payment_gateway")
        transaction_detail = cleaned_data.get("detail")
        if payment_gateway == PaymentGateway.PAYONEER:
            payment_gateway_transaction_id = payoneer_get_transaction_id(transaction_detail)
        elif payment_gateway == PaymentGateway.PAYPAL_PRO:
            payment_gateway_transaction_id = PaypalSaleService.get_transaction_id(transaction_detail)
        elif payment_gateway == PaymentGateway.PAYPAL_VAULT:
            payment_gateway_transaction_id = PaypalOrderService.get_transaction_id(transaction_detail)
        else:
            payment_gateway_transaction_id = None
        cleaned_data["payment_gateway_transaction_id"] = payment_gateway_transaction_id
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data = self.update_payment_gateway_transaction_id(cleaned_data)
        return cleaned_data

    def clean_payment_gateway(self):
        try:
            payment_gateway = self.cleaned_data.get("payment_method").payment_gateway
        except AttributeError:
            payment_gateway = self.data.get("payment_gateway")
        return payment_gateway

    def save(self, commit=True):
        instance = super().save(commit=False)

        # set content_object
        content_object = self.data.get("content_object")
        if content_object:
            instance.content_object = content_object

        if commit:
            instance.save()
        return instance


class TransactionUpdateForm(TransactionCreationForm):
    class Meta(TransactionCreationForm.Meta):
        fields = ["status", "detail", "payment_gateway_transaction_id"]

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["payment_gateway"] = self.instance.payment_gateway
        super().clean()
