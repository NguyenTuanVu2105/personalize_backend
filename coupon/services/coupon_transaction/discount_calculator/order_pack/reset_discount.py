from .base import BaseOrderPackDiscountCalculator


class OrderPackDiscountResetCalculator(BaseOrderPackDiscountCalculator):
    def __init__(self, order_obj):
        self.order = order_obj

    def update_order_pack_total_cost(self, order_pack_obj):
        pack_discount = 0
        order_pack_obj.update_costs(discount=pack_discount)
        return pack_discount

    @classmethod
    def get_discount_value(cls, cost, discount_value_obj):
        raise NotImplementedError("no discount_value is returned when call RESET calculator")

