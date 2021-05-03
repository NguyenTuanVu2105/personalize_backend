from HUB.forms.base import ModelForm
from coupon.models import CouponCampaign


class CouponCampaignForm(ModelForm):
    class Meta:
        model = CouponCampaign
        fields = ["name", "description"]
