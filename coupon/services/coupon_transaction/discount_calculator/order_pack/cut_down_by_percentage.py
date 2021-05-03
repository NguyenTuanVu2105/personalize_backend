from math import floor

from coupon.constants.coupon_values import DiscountAttribute
from .base import BaseOrderPackDiscountCalculator


class OrderPackDiscountCutDownByPercentageCalculator(BaseOrderPackDiscountCalculator):
    @classmethod
    def get_discount_value(cls, cost, discount_value_obj):
        discount_value = discount_value_obj.get(DiscountAttribute.DISCOUNT_VALUE) or 0
        max_discount_in_usd = discount_value_obj.get(DiscountAttribute.MAX_DISCOUNT_IN_USD) or 0
        assert (0 < discount_value < 100)
        assert isinstance(max_discount_in_usd, float)

        discount_in_usd = floor(cost * discount_value) / 100.0
        if 0 <= max_discount_in_usd < discount_in_usd:
            discount_in_usd = max_discount_in_usd
        return discount_in_usd
