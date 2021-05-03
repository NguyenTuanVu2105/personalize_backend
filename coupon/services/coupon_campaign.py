from django.core.exceptions import ValidationError

from coupon.forms.coupon_campaign import CouponCampaignForm


def update_or_create_coupon_campaign(request_data, existing_coupon_campaign_obj=None):
    coupon_campaign_form = CouponCampaignForm(data=request_data, instance=existing_coupon_campaign_obj)
    if not coupon_campaign_form.is_valid():
        raise ValidationError(code="coupon_campaign", message=coupon_campaign_form.errors)
    coupon_campaign_obj = coupon_campaign_form.save()
    return coupon_campaign_obj
