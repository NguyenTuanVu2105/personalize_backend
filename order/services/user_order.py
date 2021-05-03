import logging

from celery.decorators import task
from django.core.exceptions import ValidationError
from django.db import transaction

from HUB.constants.celery_task import CeleryTask
from HUB.exceptions.FormValidationError import FormValidationError
from coupon.services.coupon_transaction.coupon_redeeming import cancel_all_applied_coupon_in_order
from helper.datetime_helpers import get_current_datetime
from order.constants.fulfill_statuses import OrderPackFulfillStatus, OrderFulfillStatus
from order.forms import OrderShippingRateUpdateForm
from order.forms.order_item import UserOrderItemUpdateForm
from order.forms.order_shipping_address import UserOrderShippingAddressForm
from order.functions.save_order_items import remove_item
from order.models import FulfillmentOrderPack, Order
from order.serializers.fulfillment_order_pack import FulfillmentOrderPackSerializer
from order.services.order_cost_service import update_order_cost
from order.services.order_history import create_order_history_for_order_item_add

logger = logging.getLogger(__name__)


@transaction.atomic
def update_order(order_obj, request_data, user):
    order_updated = False
    if order_obj is None:
        raise FormValidationError(field="order", code="not_found")

    if order_obj.is_item_addable:
        add_items = request_data.get("add_items", [])
        from order.functions import save_order_item
        from order.services.service_order import split_order_packs
        if add_items:
            items = save_order_item(order_obj=order_obj, user=user, items=add_items,
                                    log_history=create_order_history_for_order_item_add)
            order_updated = True
            split_order_packs(order_obj)

    if order_obj.is_item_editable:
        update_items = request_data.pop("update_items", [])
        for item_data in update_items:
            item_id = item_data.get("id")
            order_item_obj = order_obj.items.filter(pk=item_id).first()
            if not order_item_obj:
                raise FormValidationError(field="order_item", code="not_found")
            if order_item_obj.order_pack.fulfill_status != OrderPackFulfillStatus.UNFULFILLED:
                raise FormValidationError(field="order_item", code="not_allow_edit")

            order_updated = True
            if int(item_data['quantity']) > 0:
                order_item_form = UserOrderItemUpdateForm(instance=order_item_obj, data=item_data)
                order_item_form.validate()
                order_item_form.save()
            else:
                remove_item(order_obj=order_obj, order_item_obj=order_item_obj)

    if order_obj.is_shipping_address_editable:
        shipping_address_form = UserOrderShippingAddressForm(instance=order_obj.shipping_address,
                                                             data=request_data.pop("shipping_address", {}))
        shipping_address_form.validate()
        shipping_address_form.save()
        order_updated = True
        if order_obj.fulfill_status == OrderFulfillStatus.HOLDING:
            from order.services.service_order import split_order_packs
            split_order_packs(order_obj)

    if order_obj.is_shipping_rate_editable:
        order_shipping_rate_update_form = OrderShippingRateUpdateForm(instance=order_obj,
                                                                      data=request_data.pop("shipping_rate", {}))
        order_shipping_rate_update_form.validate()
        order_shipping_rate_update_form.save()
        order_updated = True

    cancel_all_applied_coupon_in_order(order_obj)
    update_order_cost(order_obj)

    if order_updated:
        order_obj.seller_edit_time = get_current_datetime()
        order_obj.save()

    return order_obj


@task(name=CeleryTask.TASK_UPDATE_ORDER_CACHED_METADATA)
def update_order_cached_metadata_task(order_id):
    order = Order.objects.get(pk=order_id)
    update_order_cached_metadata(order)


def update_order_cached_metadata(order_obj):
    fulfillment_service_packs = FulfillmentOrderPack.objects.filter(order_pack__order__id=order_obj.id,
                                                                    tracking_number__isnull=False)
    order_obj.cached_metadata = {
        "packs": FulfillmentOrderPackSerializer(instance=fulfillment_service_packs, many=True).data
    }
    order_obj.save(update_fields=['cached_metadata'])


def update_fulfillment_settings(order_obj):
    try:
        owner = order_obj.shop.owner
        owner_settings = owner.settings
        order_obj.edit_order_items_delay = owner_settings.edit_order_items_delay
        order_obj.request_order_processing_manually = owner_settings.request_order_processing_manually
        order_obj.save()
    except Exception as e:
        raise ValidationError(str(e))
    else:
        return order_obj
