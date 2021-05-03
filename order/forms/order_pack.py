from HUB.forms.base import ModelForm
from order.models import OrderPack


class OrderPackForm(ModelForm):
    class Meta:
        model = OrderPack
        fields = ["order", "merch_pack_id", "fulfill_status", "location_id"]