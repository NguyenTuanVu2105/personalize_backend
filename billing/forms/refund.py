import decimal

from django.core.exceptions import ValidationError

from HUB.forms.base import ModelForm
from billing.constants.refund_types import RefundType
from billing.models import Refund
from order.models import Order


class RefundForm(ModelForm):
    REFUND_TYPE = RefundType.CANCEL_SHIPPING
    BASE_FEE = decimal.Decimal('0')  # USD

    def __init__(self, data, *args, **kwargs):
        assert isinstance(data, dict)
        data["refund_type"] = self.REFUND_TYPE
        super().__init__(*args, **kwargs, data=data)

    def clean_invoice(self):
        invoice_obj = self.cleaned_data["invoice"]
        if not invoice_obj.is_paid:
            raise ValidationError("Invoice are not in refundable status")
        return invoice_obj

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            raise ValidationError("")
        cleaned_data = self._clean_amount(cleaned_data)
        return cleaned_data

    def _clean_amount(self, cleaned_data):
        refund_amount = cleaned_data.get("amount")
        if not refund_amount or refund_amount <= 0:
            raise ValidationError("Invalid amount")
        invoice = cleaned_data["invoice"]
        remaining_amount = invoice.amount - refund_amount
        if remaining_amount < 0:
            raise ValidationError("Invalid amount")
        elif remaining_amount < self.BASE_FEE:
            cleaned_data["amount"] = invoice.amount - self.BASE_FEE
        return cleaned_data

    class Meta:
        model = Refund
        fields = ["user", "refund_type", "description", "amount", "status", "info"]


class CancelShippingRefundCreationForm(RefundForm):
    REFUND_TYPE = RefundType.CANCEL_SHIPPING

    class Meta(RefundForm.Meta):
        fields = ["user", "invoice", "refund_type", "description", "amount"]
        optional_fields = ["refund_type", "description"]

    def clean_description(self):
        return "Shipping cost refund"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.content_object = self.data.get("cancel_shipping_request")
        if commit:
            instance.save()
        return instance


class RejectedOrderItemsRefundCreationForm(RefundForm):
    REFUND_TYPE = RefundType.REJECT_ORDER_ITEMS

    class Meta(RefundForm.Meta):
        fields = ["user", "invoice", "refund_type", "description", "amount", "info"]
        optional_fields = ["refund_type", "description"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.content_object = self.data.get("order_obj")
        if commit:
            instance.save()
        return instance


class ManualRefundCreationForm(RefundForm):
    REFUND_TYPE = RefundType.PAY_BACK_MANUALLY

    class Meta(RefundForm.Meta):
        fields = ["user", "invoice", "refund_type", "description", "amount"]
        optional_fields = ["user", "refund_type"]

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data = self._clean_user(cleaned_data)
        cleaned_data = self._clean_order_obj(cleaned_data)
        return cleaned_data

    def _clean_user(self, cleaned_data):
        invoice = cleaned_data.get("invoice")
        if invoice:
            cleaned_data["user"] = invoice.customer
        else:
            raise ValidationError("Invalid invoice customer")
        return cleaned_data

    def _clean_order_obj(self, cleaned_data):
        order_id = self.data.get("order")
        order_obj = Order.objects.filter(id=order_id).first()
        if not order_obj:
            raise ValidationError("Invalid order")
        invoice = cleaned_data.get("invoice")
        if invoice.packs.filter(order_pack__order_id=order_obj.id).count() <= 0:
            raise ValidationError("This order is not associated with current invoice")
        self.order_obj = order_obj
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.content_object = self.order_obj
        if commit:
            instance.save()
        return instance
