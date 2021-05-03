from django.db import transaction

from billing.constants.invoice_pack_statuses import InvoicePackStatus
from order.constants.financial_statuses import OrderFinancialStatus
from order.constants.fulfill_statuses import OrderFulfillStatus, OrderPackFulfillStatus
from order.models import Order, FulfillmentOrderPack
from order.services.order_history import create_order_history_for_fulfill_status_change, \
    create_order_history_for_financial_status_change
from order.tasks import create_order_shipping_notification_task


def get_order_financial_status(order_obj):
    # CANCELLED and REJECTED statuses were removed when calculate pack_financial_statuses
    pack_financial_statuses = set(order_obj.pack_financial_statuses)
    if not pack_financial_statuses or not order_obj.packs.all() or len(pack_financial_statuses) <= 0:
        return OrderFinancialStatus.CANCELED
    if InvoicePackStatus.PAID in pack_financial_statuses:
        if len(pack_financial_statuses) > 1:
            return OrderFinancialStatus.PARTIALLY_PAID
        else:
            return OrderFinancialStatus.PAID
    elif InvoicePackStatus.UNPAID in pack_financial_statuses:
        return OrderFinancialStatus.PENDING
    elif InvoicePackStatus.FAILED in pack_financial_statuses:
        return OrderFinancialStatus.FAILED
    else:
        return OrderFinancialStatus.PENDING


@transaction.atomic
def update_order_static_financial_status(order_obj, force_reload_order_obj=True):
    if force_reload_order_obj:
        order_obj = Order.objects.include_pack_financial_statuses().filter(pk=order_obj.pk).first()
    old_financial_status = order_obj.financial_status
    new_financial_status = get_order_financial_status(order_obj)
    if new_financial_status != old_financial_status:
        order_obj.financial_status = new_financial_status
        order_obj.save()
        create_order_history_for_financial_status_change(order_obj, old_financial_status, new_financial_status)


def is_partially(statuses):
    return len(statuses) > 1


import logging

logger = logging.getLogger(__name__)


def get_order_fulfill_status(order_obj):
    pack_fulfill_statuses = order_obj.pack_fulfill_statuses

    if not pack_fulfill_statuses or not order_obj.packs.all():
        return OrderFulfillStatus.CANCELED

    if OrderPackFulfillStatus.REJECTED in pack_fulfill_statuses:
        if is_partially(pack_fulfill_statuses):
            pack_fulfill_statuses = list(
                filter(lambda status: status != OrderPackFulfillStatus.REJECTED, pack_fulfill_statuses))
        else:
            return OrderFulfillStatus.REJECTED
    if OrderPackFulfillStatus.CANCELED in pack_fulfill_statuses:
        if is_partially(pack_fulfill_statuses):
            pack_fulfill_statuses = list(
                filter(lambda status: status != OrderPackFulfillStatus.CANCELED, pack_fulfill_statuses))
        else:
            return OrderFulfillStatus.CANCELED
    if OrderPackFulfillStatus.FULFILLED in pack_fulfill_statuses:
        if is_partially(pack_fulfill_statuses):
            return OrderFulfillStatus.PARTIALLY_FULFILLED
        else:
            return OrderFulfillStatus.FULFILLED
    elif OrderPackFulfillStatus.IN_PRODUCTION in pack_fulfill_statuses:
        if len(pack_fulfill_statuses) > 1:
            return OrderFulfillStatus.PARTIALLY_IN_PRODUCTION
        else:
            return OrderFulfillStatus.IN_PRODUCTION
    elif OrderPackFulfillStatus.REQUESTED_FULFILLMENT in pack_fulfill_statuses:
        return OrderFulfillStatus.REQUESTED_FULFILLMENT
    elif OrderPackFulfillStatus.UNFULFILLED in pack_fulfill_statuses:
        return OrderFulfillStatus.UNFULFILLED
    elif OrderPackFulfillStatus.HOLDING in pack_fulfill_statuses:
        return OrderFulfillStatus.HOLDING
    elif OrderPackFulfillStatus.PENDING in pack_fulfill_statuses:
        return OrderFulfillStatus.PENDING
    elif OrderPackFulfillStatus.CANCELED in pack_fulfill_statuses:
        return OrderFulfillStatus.CANCELED
    elif OrderPackFulfillStatus.CANCELED_SHIPPING in pack_fulfill_statuses:
        return OrderFulfillStatus.CANCELED_SHIPPING
    else:
        return None


@transaction.atomic
def update_order_static_fulfill_status(order_obj, force_reload_order_obj=True):
    if force_reload_order_obj:
        order_obj = Order.objects.include_pack_fulfill_statuses().filter(pk=order_obj.pk).first()
    old_fulfill_status = order_obj.fulfill_status
    new_fulfill_status = get_order_fulfill_status(order_obj)
    if new_fulfill_status != old_fulfill_status:
        order_obj.fulfill_status = new_fulfill_status
        order_obj.save()
        create_order_history_for_fulfill_status_change(order_obj, old_fulfill_status, new_fulfill_status)
        if new_fulfill_status == OrderFulfillStatus.FULFILLED:
            transaction.on_commit(lambda: create_order_shipping_notification_task.delay(order_id=order_obj.id))


@transaction.atomic
def update_order_tracking_status(order_obj):
    fulfillment_pack_objs = FulfillmentOrderPack.objects.filter(order_pack__order_id=order_obj.pk)
    cached_metadata = order_obj.cached_metadata
    cached_metadata.update({
        "packs": list(map(lambda pack:
                          {
                              "id": pack.order_pack_id,
                              "tracking_url": pack.tracking_url,
                              "tracking_company": pack.tracking_company,
                              "tracking_status": pack.verbose_tracking_status,
                              "tracking_number": pack.tracking_number,
                              "origin_tracking_url": pack.origin_tracking_url,
                          },
                          fulfillment_pack_objs))
    })
    order_obj.cached_metadata = cached_metadata
    order_obj.save()
