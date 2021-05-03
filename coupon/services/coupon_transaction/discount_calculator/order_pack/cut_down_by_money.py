from coupon.constants.coupon_values import DiscountAttribute
from .base import BaseOrderPackDiscountCalculator


class OrderPackDiscountCutDownByMoneyCalculator(BaseOrderPackDiscountCalculator):
    @classmethod
    def get_discount_value(cls, cost, discount_value_obj):
        discount_value = discount_value_obj.get(DiscountAttribute.DISCOUNT_VALUE, cost)
        assert (0 <= discount_value <= cost)
        return discount_value
