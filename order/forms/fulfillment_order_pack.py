from HUB.forms.base import ModelForm, PreserveNotNoneInitialValueModelFormMixin
from order.models import FulfillmentOrderPack


class FulfillmentOrderPackTrackingForm(PreserveNotNoneInitialValueModelFormMixin, ModelForm):
    class Meta:
        model = FulfillmentOrderPack
        fields = ["tracking_company", "tracking_number", "tracking_url", "tracking_status", "tracking_id", "origin_tracking_url"]
        optional_fields = ["tracking_status", "origin_tracking_url"]
