import logging
from collections import defaultdict

from django.core.exceptions import ValidationError
from django.db.models import Prefetch

from billing.constants.invoice_pack_statuses import InvoicePackStatus
from billing.forms import RejectedOrderItemsRefundCreationForm
from billing.forms.refund import ManualRefundCreationForm
from billing.models import Refund
from order.constants.fulfill_statuses import OrderItemFulfillStatus
from order.models import OrderItem, Order
from order.serializers import OrderItemSerializer
from order.serializers.order_pack import OrderPackSerializer
from order.services.order_cost_service import calculate_pack_total_cost

logger = logging.getLogger(__name__)


def create_manual_refund(request_data):
    refund_form = ManualRefundCreationForm(request_data)
    if not refund_form.is_valid():
        raise ValidationError(code="refund", message=refund_form.errors)
    refund_obj = refund_form.save()
    return refund_obj


def create_refund_for_rejected_items(order_obj, rejected_item_objs, reload_order=True):
    if reload_order:
        order_obj = Order.objects.get(pk=order_obj.id)
    rejected_item_ids = [str(item.pk) for item in rejected_item_objs]
    shipping_zone, shipping_rate = order_obj.get_shipping_info()
    paid_order_pack_objs = order_obj.packs.prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.filter(fulfill_status=OrderItemFulfillStatus.ACCEPTED),
                 to_attr="accepted_items")
    ).filter(invoice_pack__status=InvoicePackStatus.PAID)

    refund_amount_container = defaultdict(lambda: 0)
    refund_info = defaultdict(lambda: {"items": [], "packs": []})
    for pack_obj in paid_order_pack_objs:
        rejected_items_in_pack = [i for i in rejected_item_objs if i.order_pack.id == pack_obj.id]
        if len(rejected_items_in_pack) == 0:
            continue
        total_cost = pack_obj.total_cost
        accepted_total_cost = calculate_pack_total_cost(pack_obj.accepted_items, shipping_zone, shipping_rate)
        # TODO include previous refunds + idempotency key for preventing duplication
        refund_amount = total_cost - accepted_total_cost
        invoice_id = pack_obj.invoice_pack.invoice_id
        refund_amount_container[invoice_id] += refund_amount
        refund_info[invoice_id]["items"] += OrderItemSerializer(instance=rejected_items_in_pack, many=True).data
        refund_info[invoice_id]["packs"] += OrderPackSerializer(instance=pack_obj).data

    for invoice_id, refund_amount in refund_amount_container.items():
        if Refund.objects.filter(invoice_id=invoice_id).count() > 0:
            continue
        refund_form = RejectedOrderItemsRefundCreationForm(
            {"user": order_obj.shop.owner_id, "amount": refund_amount,
             "order_obj": order_obj, "invoice": invoice_id, "info": refund_info[invoice_id],
             "description": "Rejected Order Item IDs: {}".format(",".join(rejected_item_ids))})
        if refund_form.is_valid():
            refund_form.save()
        else:
            raise ValidationError(code="refund", message=refund_form.errors)
    return order_obj
