import logging

from django.db import transaction

from coupon.services.coupon_transaction.discount_calculator.order_pack.manager import OrderPackDiscountCalculatorManager
from order.constants.fulfill_statuses import OrderPackFulfillStatus, OrderFulfillStatus
from order.models import OrderItem, Order

logger = logging.getLogger(__name__)


@transaction.atomic
def update_order_cost(order_obj, reload_order=False):
    if reload_order:
        order_obj = Order.objects.get(pk=order_obj.id)
    if order_obj.fulfill_status != OrderFulfillStatus.UNFULFILLED:
        logger.info("Order has been fulfilled. Ignore Pricing")
        return order_obj
    total_order_production_cost = 0
    total_order_shipping_cost = 0
    shipping_zone, shipping_rate = order_obj.get_shipping_info()
    for pack in order_obj.packs.all():
        if pack.fulfill_status != OrderPackFulfillStatus.UNFULFILLED:
            continue
        items, production_cost, shipping_cost = calculate_pack_cost(items=pack.items.join_abstract_variant(),
                                                                    shipping_zone=shipping_zone,
                                                                    shipping_rate=shipping_rate)
        OrderItem.objects.bulk_update(items, ['production_cost', 'base_cost', 'extra_cost'])
        pack.update_costs(production_cost=production_cost, shipping_cost=shipping_cost, discount=0)
        total_order_production_cost += production_cost
        total_order_shipping_cost += shipping_cost

    order_obj.update_costs(production_cost=total_order_production_cost, shipping_cost=total_order_shipping_cost,
                           discount=0)
    OrderPackDiscountCalculatorManager.update_total_cost(order_obj)
    return order_obj


def calculate_pack_cost(items, shipping_zone, shipping_rate):
    max_base_shipping_cost = 0
    max_additional_shipping_cost = 0
    total_pack_quantity = 0
    total_pack_production_cost = 0
    for item in items:
        quantity = item.quantity
        extra_cost = item.user_variant.user_product.extra_cost
        shipping_cost = item.get_shipping_cost_abstract_variant_obj(shipping_zone, shipping_rate)

        base_cost = shipping_cost.production_cost_base
        additional_cost = shipping_cost.production_cost_additional

        production_cost = min(1, quantity) * base_cost + max(0, quantity - 1) * additional_cost + max(0,
                                                                                                      quantity) * extra_cost
        item.production_cost = production_cost
        item.base_cost = base_cost
        item.extra_cost = extra_cost
        total_pack_quantity += max(0, quantity)
        total_pack_production_cost += production_cost

        max_base_shipping_cost = max(max_base_shipping_cost, shipping_cost.shipping_cost_base)
        max_additional_shipping_cost = max(max_additional_shipping_cost, shipping_cost.shipping_cost_additional)
    # Update pack cost
    pack_shipping_cost = min(1, total_pack_quantity) * max_base_shipping_cost + max(0,
                                                                                    total_pack_quantity - 1) * max_additional_shipping_cost
    return items, total_pack_production_cost, pack_shipping_cost


def calculate_pack_total_cost(items, shipping_zone, shipping_rate):
    _, total_pack_production_cost, pack_shipping_cost = calculate_pack_cost(items, shipping_zone, shipping_rate)
    return total_pack_production_cost + pack_shipping_cost
