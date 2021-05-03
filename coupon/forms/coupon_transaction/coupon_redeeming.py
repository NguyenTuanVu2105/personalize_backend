from django.core.exceptions import FieldError, ValidationError
from django.db import transaction

from coupon.forms.coupon_transaction.base import CouponTransactionForm
from coupon.models import Coupon, RedeemedCouponTransaction
from coupon.services.coupon_transaction.extra_constraint_validating_services.coupon_mapping_manager import \
    CouponValidatorMappingManager
from coupon.services.coupon_transaction.coupon_transaction_idempotency import CouponTransactionIdempotencyService
from coupon.services.coupon_transaction.discount_calculator.order_pack.manager import OrderPackDiscountCalculatorManager
from helper.datetime_helpers import get_current_datetime


class CouponRedeemingForm(CouponTransactionForm):
    @transaction.atomic
    def save(self):
        transaction_obj = RedeemedCouponTransaction.objects.create(user=self.user, coupon=self.coupon, order=self.order,
                                                                   idempotency_key=self.transaction_idempotency_key,
                                                                   redeemed_detail={})
        OrderPackDiscountCalculatorManager.update_total_cost(self.order, self.coupon)
        return transaction_obj

    def clean(self):
        super().clean()
        if self.errors:
            return
        try:
            self.check_basic_coupon_rules()
            self.check_user_coupon_rules()
            self.check_coupon_extra_constraint_rules()
        except (FieldError, AssertionError):
            pass

    def check_basic_coupon_rules(self):
        code = self.cleaned_data.get("code")
        try:
            coupon_obj = Coupon.objects.include_redeemed_count().get(code=code)
        except Coupon.DoesNotExist:
            self.add_error("code", "This code is not valid")
            raise FieldError
        else:
            current_time = get_current_datetime()
            if coupon_obj.valid_until < current_time:
                self.add_error("code", "This code has expired")
                raise FieldError
            if coupon_obj.redeemed_count >= coupon_obj.redeeming_limit:
                self.add_error("code", "This code has reached maximum usage")
                raise FieldError
            self.coupon = coupon_obj

    def check_user_coupon_rules(self):
        """
        implementation for basic case only:
        each user + coupon = 1 time
        => idempotency_key = user_id + coupon_id
        """

        user_id = self.user.id
        coupon_id = self.coupon.id

        assert self.order
        order_id = self.order.id
        coupon_idempotency_service = CouponTransactionIdempotencyService(user_id=user_id, coupon_id=coupon_id,
                                                                         order_id=order_id)
        idempotency_key = coupon_idempotency_service.get_key_by_user()
        if RedeemedCouponTransaction.objects.filter(idempotency_key=idempotency_key).exists():
            self.add_error("code", "This code has been already redeemed")
            raise FieldError
        if RedeemedCouponTransaction.objects.filter(order_id=order_id).exists():
            self.add_error("code", "Each order could be applied with one coupon in maximum")
            raise FieldError
        self.transaction_idempotency_key = idempotency_key

    def check_coupon_extra_constraint_rules(self):
        validating_service_cls = CouponValidatorMappingManager.get_service_cls(self.coupon.constraint_validating_type)
        validating_service = validating_service_cls(user=self.user, coupon=self.coupon, order=self.order)

        try:
            validating_service.verify()
        except ValidationError as e:
            self.add_error(e.code, e.message)
            raise FieldError
