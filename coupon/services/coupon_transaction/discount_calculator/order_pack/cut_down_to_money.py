from coupon.constants.coupon_values import DiscountAttribute
from .base import BaseOrderPackDiscountCalculator


class OrderPackDiscountCutDownToMoneyCalculator(BaseOrderPackDiscountCalculator):
    @classmethod
    def get_discount_value(cls, cost, discount_value_obj):
        discount_value = discount_value_obj.get(DiscountAttribute.DISCOUNT_VALUE) or 0
        assert (0 <= discount_value <= cost)
        return cost - discount_value
