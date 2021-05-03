from django.core.exceptions import ValidationError

from coupon.forms.coupon_transaction.coupon_canceling import CouponCancelingForm
from coupon.forms.coupon_transaction.coupon_redeeming import CouponRedeemingForm
from coupon.models import RedeemedCouponTransaction


def redeem_coupon_by_user_request(request_data, user):
    coupon_redeeming_form = CouponRedeemingForm(data=request_data, user=user)
    if not coupon_redeeming_form.is_valid():
        raise ValidationError(code="coupon", message=coupon_redeeming_form.errors)
    coupon_redeeming_form.save()


def cancel_coupon_by_user_request(request_data, user):
    coupon_canceling_form = CouponCancelingForm(data=request_data, user=user)
    if not coupon_canceling_form.is_valid():
        raise ValidationError(code="coupon", message=coupon_canceling_form.errors)
    coupon_canceling_form.save()


def cancel_all_applied_coupon_in_order(order_obj):
    RedeemedCouponTransaction.objects.filter(order_id=order_obj.id).delete()
