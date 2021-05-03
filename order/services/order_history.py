from helper.encoders import JSONEncoder
from order.constants.order_history_types import OrderHistoryType
from order.models import OrderHistory
from order.models.order import get_verbose_fulfill_status, get_verbose_financial_status
from order.serializers import OrderItemSerializer
from order.serializers.order_shipping_address import OrderShippingAddressSerializer
from support.serializers.ticket_support_serializer import BriefTicketSupportSerializer
from user_product.serializers import UserVariantSerializer


def create_order_history_for_new_order(order_obj):
    old_obj = {}
    new_obj = {}
    message = "Order had been created"
    create_order_history(order_obj.id, OrderHistoryType.CREATE_ORDER, message, old_obj, new_obj)


def create_order_history_for_shipping_rate_change(order_obj, old_value, new_value):
    old_obj = {"shipping_rate": old_value}
    new_obj = {"shipping_rate": new_value}
    message = "Order's shipping rate had been changed"
    create_order_history(order_obj.id, OrderHistoryType.UPDATE_ORDER_SHIPPING_RATE, message, old_obj, new_obj)


def create_order_history_for_fulfill_status_change(order_obj, old_status, new_status):
    old_obj = {"fulfill_status": get_verbose_fulfill_status(old_status)}
    new_obj = {"fulfill_status": get_verbose_fulfill_status(new_status)}
    message = "Order's fulfillment status had been changed"
    create_order_history(order_obj.id, OrderHistoryType.UPDATE_ORDER_FULFILL_STATUS, message, old_obj, new_obj)


def create_order_history_for_financial_status_change(order_obj, old_status, new_status):
    old_obj = {"financial_status": get_verbose_financial_status(old_status)}
    new_obj = {"financial_status": get_verbose_financial_status(new_status)}
    message = "Order's financial status had been changed"
    create_order_history(order_obj.id, OrderHistoryType.UPDATE_ORDER_FINANCIAL_STATUS, message, old_obj, new_obj)


def create_order_history_for_is_item_editable_change(order_obj, old_status, new_status):
    message = "Order items had been restricted by Fulfillment Service"
    create_order_history(order_obj.id, OrderHistoryType.UPDATE_ORDER_IS_ITEM_EDITABLE_STATUS, message, {}, {})


def create_order_history_for_order_item_user_variant_change(order_obj, old_variant_obj, new_variant_obj):
    base_obj = {"order_id": order_obj.id}
    old_obj = {**base_obj, "variant": UserVariantSerializer(old_variant_obj).data}
    new_obj = {**base_obj, "variant": UserVariantSerializer(new_variant_obj).data}
    message = "Order item's variant had been changed"
    create_order_history(order_obj.id, OrderHistoryType.UPDATE_ORDER_ITEM_VARIANT, message, old_obj, new_obj)


def create_order_history_for_order_item_quantity_change(order_obj, old_order_item_obj, new_order_item_obj):
    base_obj = {"order_id": order_obj.id}
    old_obj = {**base_obj, "order_item": OrderItemSerializer(old_order_item_obj).data}
    new_obj = {**base_obj, "order_item": OrderItemSerializer(new_order_item_obj).data}
    message = "Order item's quantity had been changed"
    create_order_history(order_obj.id, OrderHistoryType.UPDATE_ORDER_ITEM_QUANTITY, message, old_obj, new_obj)


def create_order_history_for_order_item_remove(order_obj, order_item_obj):
    base_obj = {"order_id": order_obj.id}
    old_obj = {**base_obj, "order_item": OrderItemSerializer(order_item_obj).data}
    new_obj = {}
    message = "Order item had been removed"
    create_order_history(order_obj.id, OrderHistoryType.REMOVE_ORDER_ITEM, message, old_obj, new_obj)


def create_order_history_for_order_item_add(order_obj, order_item_obj):
    base_obj = {"order_id": order_obj.id}
    old_obj = {}
    new_obj = {**base_obj, "order_item": OrderItemSerializer(order_item_obj).data}
    message = "Order item had been added"
    create_order_history(order_obj.id, OrderHistoryType.ADD_ORDER_ITEM, message, old_obj, new_obj)


def create_order_history_for_shipping_address_change(order_obj, old_shipping_address_obj, new_shipping_address_obj,
                                                     is_approved):
    base_obj = {"order_id": order_obj.id}
    old_obj = {**base_obj, "shipping_address": OrderShippingAddressSerializer(old_shipping_address_obj).data}
    new_obj = {**base_obj, "shipping_address": OrderShippingAddressSerializer(new_shipping_address_obj).data}
    message = "Order's shipping address had been changed"
    create_order_history(order_obj.id, OrderHistoryType.UPDATE_ORDER_SHIPPING_ADDRESS, message, old_obj, new_obj,
                         is_approved)


def create_order_history_for_new_support_ticket(order_obj, ticket):
    ticket_obj = BriefTicketSupportSerializer(instance=ticket).data
    message = f"Ticket #{ticket.ticket_id} support created"
    create_order_history(order_obj.id, OrderHistoryType.CREATE_SUPPORT_TICKET, message, {}, ticket_obj)


def create_order_history_for_resolved_support_ticket_status(order_obj, ticket):
    ticket_obj = BriefTicketSupportSerializer(instance=ticket).data
    message = f"Ticket #{ticket.ticket_id} support resolved"
    create_order_history(order_obj.id, OrderHistoryType.UPDATE_SUPPORT_TICKET, message, {}, ticket_obj)


def create_order_history_for_fulfill_reject_items(order_obj, rejected_items):
    if len(rejected_items) == 0:
        return
    new_obj = {"rejected_items": OrderItemSerializer(instance=rejected_items, many=True).data}
    sku_list_as_str = ", ".join(list(map(lambda item: item.user_variant.sku, rejected_items)))
    message = f"Fulfillment Service has rejected {len(rejected_items)} items with SKU {sku_list_as_str}"
    create_order_history(order_obj.id, OrderHistoryType.REJECT_ITEM_BY_FULFILL, message, {}, new_obj)


def create_order_history_for_reject_not_support_shipping_items(order_obj, rejected_items):
    if len(rejected_items) == 0:
        return
    new_obj = {"rejected_items": OrderItemSerializer(instance=rejected_items, many=True).data}
    sku_list_as_str = ", ".join(list(map(lambda item: item.user_variant.sku, rejected_items)))
    message = f"Fulfillment Service has rejected {len(rejected_items)} items with SKU {sku_list_as_str}. Reject reason: Not Support Shipping"
    create_order_history(order_obj.id, OrderHistoryType.REJECT_NOT_SUPPORT_SHIPPING_ITEM, message, {}, new_obj)


def create_order_history_for_reject_no_shipping_items(order_obj, rejected_items):
    if len(rejected_items) == 0:
        return
    new_obj = {"rejected_items": OrderItemSerializer(instance=rejected_items, many=True).data}
    sku_list_as_str = ", ".join(list(map(lambda item: item.user_variant.sku, rejected_items)))
    message = f"Fulfillment Service has rejected {len(rejected_items)} items with SKU {sku_list_as_str}. Reject reason: No Customer or Shipping Address"
    create_order_history(order_obj.id, OrderHistoryType.REJECT_NO_SHIPPING_ITEM, message, {}, new_obj)


def create_order_history_for_fulfill_reject(order_obj, reason="Invalid order"):
    if not reason:
        reason = "Invalid order"
    message = f"Fulfillment service has rejected order with reason: " + reason
    create_order_history(order_obj.id, OrderHistoryType.REJECT_ORDER_BY_FULFILL, message, {}, {"reason": reason})


def create_order_history(order_id, history_type, message, old_obj, new_obj, is_approved=True):
    old_obj = JSONEncoder().default(old_obj)
    new_obj = JSONEncoder().default(new_obj)
    OrderHistory.objects.create(order_id=order_id, type=history_type, message=message, old_obj=old_obj,
                                new_obj=new_obj, is_approved=is_approved)
