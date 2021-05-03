from order.constants.fulfill_statuses import OrderFulfillStatus


def check_ticket_order_change_size_color(orders):
    list_change = [OrderFulfillStatus.PENDING, OrderFulfillStatus.UNFULFILLED,
                   OrderFulfillStatus.REQUESTED_FULFILLMENT, OrderFulfillStatus.REJECTED, OrderFulfillStatus.CANCELED]
    result = []
    for order in orders:
        if not order.fulfill_status in list_change:
            result.append(order.id)
    return result


def check_ticket_order_change_address(orders):
    list_not_change = [OrderFulfillStatus.FULFILLED, OrderFulfillStatus.PARTIALLY_FULFILLED]
    result = []
    for order in orders:
        if order.fulfill_status in list_not_change:
            result.append(order.id)
    return result
