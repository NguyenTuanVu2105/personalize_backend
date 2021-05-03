from django.core.exceptions import ValidationError

from coupon.forms.coupon import CouponForm


def update_or_create_coupon(request_data, existing_coupon_obj=None):
    coupon_form = CouponForm(data=request_data, instance=existing_coupon_obj)
    if not coupon_form.is_valid():
        raise ValidationError(code="coupon", message=coupon_form.errors)
    coupon_obj = coupon_form.save()
    return coupon_obj
