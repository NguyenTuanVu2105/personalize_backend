from django.core.exceptions import FieldError
from django.db import transaction

from coupon.forms.coupon_transaction.base import CouponTransactionForm
from coupon.models import Coupon, RedeemedCouponTransaction
from coupon.services.coupon_transaction.coupon_transaction_idempotency import CouponTransactionIdempotencyService
from coupon.services.coupon_transaction.discount_calculator.order_pack.reset_discount import \
    OrderPackDiscountResetCalculator


class CouponCancelingForm(CouponTransactionForm):
    def clean(self):
        super().clean()
        if self.errors:
            return
        try:
            self.check_basic_coupon_rules()
        except (FieldError, AssertionError):
            pass

    def check_basic_coupon_rules(self):
        code = self.cleaned_data['code']
        try:
            coupon_obj = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            self.add_error("code", "This code is not valid")
            raise FieldError
        else:
            self.coupon = coupon_obj

    @transaction.atomic
    def save(self):
        user_id = self.user.id
        coupon_id = self.coupon.id

        assert self.order
        order_id = self.order.id
        coupon_idempotency_service = CouponTransactionIdempotencyService(user_id=user_id, coupon_id=coupon_id,
                                                                         order_id=order_id)
        idempotency_key = coupon_idempotency_service.get_key_by_user()
        transaction_count, *_ = RedeemedCouponTransaction.objects.filter(idempotency_key=idempotency_key).delete()
        if transaction_count > 0:
            OrderPackDiscountResetCalculator(self.order).update_order_total_cost()
