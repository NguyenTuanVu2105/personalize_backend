from coupon.constants.discount_types import DiscountType
from .cut_down_by_money import OrderPackDiscountCutDownByMoneyCalculator
from .cut_down_by_percentage import OrderPackDiscountCutDownByPercentageCalculator
from .cut_down_to_money import OrderPackDiscountCutDownToMoneyCalculator


class OrderPackDiscountCalculatorManager:
    CALCULATOR_MAPPING = {
        DiscountType.MONETARY_CUT_DOWN_BY_VALUE: OrderPackDiscountCutDownByMoneyCalculator,
        DiscountType.MONETARY_CUT_DOWN_TO_VALUE: OrderPackDiscountCutDownToMoneyCalculator,
        DiscountType.PERCENTAGE_CUT_DOWN_BY_VALUE: OrderPackDiscountCutDownByPercentageCalculator
    }

    @classmethod
    def update_total_cost(cls, order_obj, coupon_obj=None):
        # if coupon_obj is not passed as parameter
        # -> all applied coupons in order will be retrieve for further calculating
        if not coupon_obj:
            coupon_obj = order_obj.applied_coupons.first()
            # if no coupon_obj was found, calculating phase will be terminated
            if not coupon_obj:
                return

        discount_type = coupon_obj.discount_type
        calculator_cls = cls.CALCULATOR_MAPPING.get(discount_type)
        calculator_cls(order_obj, coupon_obj).update_order_total_cost()
