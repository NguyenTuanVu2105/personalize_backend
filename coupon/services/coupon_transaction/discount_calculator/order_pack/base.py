from django.db import transaction

from coupon.constants.coupon_values import DiscountTarget


class BaseOrderPackDiscountCalculator:
    def __init__(self, order_obj, coupon_obj):
        self.order = order_obj
        self.discount_type = coupon_obj.discount_type
        self.discount_values = coupon_obj.value_config

    @transaction.atomic
    def update_order_total_cost(self):
        order_obj = self.order
        order_pack_objs = order_obj.packs.all()
        order_total_discount = 0
        for pack_obj in order_pack_objs:
            pack_discount = self.update_order_pack_total_cost(pack_obj)
            order_total_discount += pack_discount
        order_obj.update_costs(discount=order_total_discount)

    def update_order_pack_total_cost(self, order_pack_obj):
        pack_discount = self.get_order_pack_discount(order_pack_obj)
        order_pack_obj.update_costs(discount=pack_discount)
        return pack_discount

    def get_order_pack_discount(self, order_pack_obj):
        pack_production_cost_discount = self.calculate_discount(order_pack_obj.production_cost,
                                                                self.discount_values.get(
                                                                    DiscountTarget.PACK_PRODUCTION_COST))
        pack_shipping_cost_discount = self.calculate_discount(order_pack_obj.shipping_cost, self.discount_values.get(
            DiscountTarget.PACK_SHIPPING_COST))
        pack_discount = pack_production_cost_discount + pack_shipping_cost_discount
        return pack_discount

    @classmethod
    def calculate_discount(cls, cost, discount_value_obj):
        if not discount_value_obj:
            return 0
        return min(cls.get_discount_value(cost, discount_value_obj), cost)

    @classmethod
    def get_discount_value(cls, cost, discount_value_obj):
        raise NotImplementedError("method get_discount_value is not implemented")
