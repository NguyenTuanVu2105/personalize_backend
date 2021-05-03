import logging

from HUB.forms.base import PreserveNotNoneInitialValueModelForm
from user.models import UserSettings

logger = logging.getLogger(__name__)
from django.forms import ValidationError


class UserSettingsForm(PreserveNotNoneInitialValueModelForm):
    class Meta:
        model = UserSettings
        fields = (
            "timezone", "tracking_generation_time", "request_order_processing_manually", "edit_order_items_delay",)

    def clean_edit_order_items_delay(self):
        edit_order_items_delay = self.data["edit_order_items_delay"]
        if edit_order_items_delay < 0 or edit_order_items_delay > 172800:
            raise ValidationError("Processing time must be less than 2 days")
        return self.cleaned_data["edit_order_items_delay"]
