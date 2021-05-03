from django.utils import timezone

from HUB.forms.base import ModelForm
from order.models import CancelShippingRequest


class CancelShippingRequestForm(ModelForm):
    class Meta:
        model = CancelShippingRequest
        fields = ["user", "note", "approve_time"]


class CancelShippingRequestCreationForm(CancelShippingRequestForm):
    class Meta(CancelShippingRequestForm.Meta):
        fields = ["user", "note", "order_packs", "order"]


class CancelShippingRequestHandleForm(CancelShippingRequestForm):
    class Meta(CancelShippingRequestForm.Meta):
        fields = ["admin", "admin_note", "approve_time", "status"]
        optional_fields = ["approve_time"]

    def clean_approve_time(self):
        return timezone.now()

    def clean_status(self):
        status = self.cleaned_data["status"]
        if self.instance and not self.instance.is_pending:
            self.add_error("status", "Can't change approved form")
        return status
