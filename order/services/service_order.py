import logging
import traceback
from collections import defaultdict, OrderedDict

from celery.decorators import task
from django.core.exceptions import ValidationError
from django.db import transaction

from HUB.constants.celery_task import CeleryTask
from HUB.exceptions.FormValidationError import FormValidationError
from admin_tools.constants import SystemSettingTypes
from admin_tools.models import SystemSetting
from billing.models import Refund
from billing.services import InvoiceService
from billing.services.refund import create_refund_for_rejected_items
from helper.datetime_helpers import get_current_datetime
from notification.enums.message_types import MessageType
from notification.models import Template
from notification.services import send_notification_task
from notification.services.notification import send_user_email, send_admin_notification
from order.constants.fulfill_statuses import OrderPackFulfillStatus, OrderFulfillStatus, OrderItemFulfillStatus
from order.forms import CustomerInfoForm, OrderForm, OrderPackForm, OrderItemForm
from order.forms.order_shipping_address import OrderShippingAddressForm
from order.models import Order, OrderItem, OrderPack, FulfillmentOrderPack, OrderHolding
from order.services.order_status import update_order_static_fulfill_status, update_order_static_financial_status
from service_communication.services.adapter_services import AdapterOrderCommunicationService
from service_communication.services.fulfill_services import FulfillOrderCommunicationService
from shop.constants.shop_status import ShopStatus
from shop.models import Shop
from support.constants.ticket_statuses import SupportTicketStatus
from system_metadata.constants import DEFAULT_CURRENCY
from user_product.functions.update_fulfill_artwork import sync_artwork_by_shop
from user_product.models import UserVariant, UserProductArtworkFusion, UserVariantPrice
from .order_cost_service import update_order_cost, calculate_pack_cost
from .order_history import create_order_history_for_is_item_editable_change, \
    create_order_history_for_reject_not_support_shipping_items, create_order_history_for_fulfill_reject_items, \
    create_order_history_for_reject_no_shipping_items, create_order_history_for_fulfill_reject
from .order_pack_status import update_order_packs_static_fulfill_status
from .user_order import update_order_cached_metadata_task, update_fulfillment_settings
from ..constants.financial_statuses import OrderFinancialStatus
from ..constants.invalid_reason_types import InvalidReasonType
from ..forms.order_item import BrandingCardOrderItemForm
from ..functions.traceback_order_invalid import traceback_order_invalid, is_valid_exist_order, is_valid_shop, \
    is_valid_paid, is_valid_items
from ..models.order_invallid import OrderInvalid
from ..serializers.order_cost_serializer import SampleOrderPack

logger = logging.getLogger(__name__)

NO_SHIPPING = -2
NOT_SHIPPING_PROVIDE = -1
NO_ABSTRACT_SKU = -3
INIT_PACK = 1


def is_valid_order(request_data):
    if not is_valid_exist_order(request_data):
        return False
    if not is_valid_shop(request_data):
        return False
    if not is_valid_paid(request_data):
        return False
    if not is_valid_items(request_data):
        return False
    return True


def create_order(request_data):
    if is_valid_order(request_data):
        shop = Shop.objects.filter(url=request_data.get("shop_url"), status=ShopStatus.ACTIVE).first()
        shop.reset_api_error_count()
        create_valid_order(request_data)
    else:
        raise FormValidationError(field='order', code="invalid")


def create_valid_order(request_data):
    try:
        order_obj = initialize_new_order(request_data)
    except Exception as e:
        logger.exception(e)
        traceback.print_tb(e.__traceback__)
        traceback_order_invalid(request_data, InvalidReasonType.OTHER, str(e))
        raise Exception(e)
    split_order_packs(order_obj)
    update_order_cost(order_obj, reload_order=True)


@transaction.atomic()
def initialize_new_order(request_data):
    order_id = request_data['order_id']
    if Order.objects.filter(order_id=order_id).exists():
        raise FormValidationError(field="order", code="existed")
    customer_data = request_data.get("customer", {})
    if customer_data.get("customer_id"):
        customer_info_form = CustomerInfoForm(data=request_data.get("customer"))
        customer_info_form.validate()
        customer_info_obj = customer_info_form.save()
        customer_info_pk = customer_info_obj.pk
    else:
        customer_info_pk = None

    shipping_address_form = OrderShippingAddressForm(data=request_data.get("shipping_address"))
    shipping_address_form.validate()
    shipping_address = shipping_address_form.save()

    items = request_data.get("items")
    order_form = OrderForm(
        data={**request_data,
              "customer_info": customer_info_pk,
              "shipping_address": shipping_address.pk,
              "country_code": shipping_address.country_code,
              "seller_edit_time": get_current_datetime(),
              "total_items": len(items)})
    order_form.validate()
    order_obj = order_form.save()

    item_count = 0
    for item in items:
        item["order"] = order_obj.pk
        item["item_id"] = item["id"]
        item["shop_url"] = request_data["shop_url"]
        order_item_form = OrderItemForm(data=item)
        if order_item_form.is_valid():
            order_item_form.save()
            item_count += 1
    if item_count <= 0:
        raise ValidationError(code="order_item", message={"user_variant": "Invalid order items"})
    if item_count < len(items):
        traceback_order_invalid(request_data, InvalidReasonType.PARTIAL_ITEM_IN_PRINTHOLO)

    append_order_branding_card(order_obj)
    update_fulfillment_settings(order_obj)

    return order_obj


# @transaction.atomic
def append_order_branding_card(order_obj):
    try:
        shop = order_obj.shop
        owner = shop.owner
        default_branding_card = owner.settings.default_branding_card
        if default_branding_card and not order_obj.has_branding_card_item:
            item_data = {
                "order": order_obj.pk,
                # "order_pack": order_pack_obj.pk,
                "item_id": default_branding_card.id,
                "price": UserVariantPrice.objects.get(user_variant=default_branding_card,
                                                      currency=DEFAULT_CURRENCY).value,
                "currency": DEFAULT_CURRENCY,
                "user_variant": default_branding_card.id,
            }
            order_item_form = BrandingCardOrderItemForm(data=item_data)
            order_item_form.validate()
            if order_item_form.is_valid():
                order_item_form.save()
    except Exception as e:
        logger.error(f'Can not automatically append branding card for order: {order_obj.id}')
        logger.exception(str(e))


@transaction.atomic
def split_order_packs(order_obj):
    order_items_objs = order_obj.items.join_abstract_variant()
    shipping_zone, shipping_rate = order_obj.get_shipping_info()
    packs_dict = defaultdict(list)
    branding_card_item = None
    for item_obj in order_items_objs:
        abstract_sku = item_obj.user_variant.abstract_variant.product.sku
        if not shipping_zone:
            key = NO_SHIPPING
        elif not item_obj.is_shipping_supported(shipping_zone, shipping_rate):
            key = NOT_SHIPPING_PROVIDE
        elif not abstract_sku:
            key = NO_ABSTRACT_SKU
        elif item_obj.is_branding_card_item:
            branding_card_item = item_obj
            continue
        else:
            key = abstract_sku
        packs_dict[key].append(item_obj)

    # append branding card item to first pack
    if branding_card_item:
        pack = list(packs_dict.keys())[0] if len(packs_dict.keys()) > 0 else INIT_PACK
        packs_dict[pack].append(branding_card_item)

    sorted_packs_dict = OrderedDict(sorted(packs_dict.items()))
    new_packs = []
    for key, item_objs in sorted_packs_dict.items():
        fulfill_status = OrderPackFulfillStatus.UNFULFILLED
        if key == NOT_SHIPPING_PROVIDE:
            OrderItem.objects.filter(id__in=[item.pk for item in item_objs]).bulk_set_holding_fulfillment()
            create_order_history_for_reject_not_support_shipping_items(order_obj, item_objs)
            fulfill_status = OrderPackFulfillStatus.HOLDING
        elif key == NO_SHIPPING:
            OrderItem.objects.filter(id__in=[item.pk for item in item_objs]).bulk_set_holding_fulfillment()
            create_order_history_for_reject_no_shipping_items(order_obj, item_objs)
            fulfill_status = OrderPackFulfillStatus.HOLDING
        else:
            OrderItem.objects.filter(id__in=[item.pk for item in item_objs]).bulk_set_accept_fulfillment()
        order_pack_form = OrderPackForm(
            data={"order": order_obj.pk, "location_id": order_obj.shop.location_id, "fulfill_status": fulfill_status})
        order_pack_form.validate()
        order_pack = order_pack_form.save()
        order_pack.items.set(item_objs)
        order_pack.save()
        new_packs.append(order_pack)

    # Clear empty packs
    OrderPack.objects.filter(order__id=order_obj.id, items=None).delete()
    transaction.on_commit(lambda: update_order_packs_static_fulfill_status(order_obj, updated_pack_objs=new_packs))
    transaction.on_commit(lambda: update_order_static_financial_status(order_obj))
    # transaction.on_commit(lambda: sync_new_packs(order_obj))


def split_order_items(items, shipping_zone, shipping_rate):
    packs_dict = defaultdict(list)
    for item_obj in items:
        abstract_sku = item_obj.user_variant.abstract_variant.product.sku
        if not shipping_zone:
            key = NO_SHIPPING
        elif not item_obj.is_shipping_supported(shipping_zone, shipping_rate):
            key = NOT_SHIPPING_PROVIDE
        elif not abstract_sku:
            key = NO_ABSTRACT_SKU
        else:
            key = abstract_sku
        packs_dict[key].append(item_obj)

    sorted_packs_dict = OrderedDict(sorted(packs_dict.items()))
    new_packs = []
    for key, item_objs in sorted_packs_dict.items():
        pack = SampleOrderPack()
        if key in [NOT_SHIPPING_PROVIDE, NO_SHIPPING]:
            pack.fulfill_status = OrderPackFulfillStatus.REJECTED
        else:
            pack.fulfill_status = OrderPackFulfillStatus.UNFULFILLED
        pack.items = item_objs
        new_packs.append(pack)
    return new_packs


def calculate_fake_order(items, shipping_zone, shipping_rate):
    packs = split_order_items(items, shipping_zone, shipping_rate)
    total_order_production_cost = 0
    total_order_shipping_cost = 0
    for pack in packs:
        if pack.fulfill_status != OrderPackFulfillStatus.UNFULFILLED:
            continue
        items, production_cost, shipping_cost = calculate_pack_cost(items=pack.items,
                                                                    shipping_zone=shipping_zone,
                                                                    shipping_rate=shipping_rate)
        pack.shipping_cost = shipping_cost
        pack.production_cost = production_cost
        pack.total_cost = production_cost + shipping_cost

        total_order_production_cost += pack.production_cost
        total_order_shipping_cost += pack.shipping_cost
    return packs, total_order_production_cost, total_order_shipping_cost


@transaction.atomic
def update_order(request_data):
    order_id = request_data['order_id']
    order = Order.objects.filter(order_id=order_id).first()
    if not order:
        # process order unpaid => paid
        order_invalid = OrderInvalid.objects.filter(order_id=order_id).first()
        if order_invalid:
            order_paid = request_data.get('financial_status') == 'paid'
            if order_invalid.reason_code == InvalidReasonType.UNPAID_ORDER and order_paid:
                create_valid_order(request_data)
    elif order.is_shipping_address_editable:
        # Update Shipping Address
        shipping_address_form = OrderShippingAddressForm(instance=order.shipping_address,
                                                         data=request_data['shipping_address'])
        shipping_address_form.validate()
        shipping_address_form.save()
        if order.is_shipping_city_editable:
            order.seller_edit_time = get_current_datetime()
            order.save()


@transaction.atomic
def process_order(order_obj, request_data):
    order_item_objs = order_obj.items.select_related("order_pack").filter(
        order_pack__fulfill_status=OrderPackFulfillStatus.REQUESTED_FULFILLMENT)
    order_item_obj_dict = {}
    order_item_obj_rejected_flag = {}
    for item_obj in order_item_objs:
        user_variant_id = item_obj.user_variant_id
        order_item_obj_dict[user_variant_id] = item_obj
        order_item_obj_rejected_flag[user_variant_id] = True
    fulfillment_pack_cost = 0
    for pack_data in request_data["fulfillments"]:
        mfr_pack_id = pack_data["id"]
        order_pack_ids = set()
        for index, item_data in enumerate(pack_data["items"]):
            variant_sku = item_data["variant"]
            user_variant_obj = UserVariant.objects.select_related("abstract_variant").filter(sku=variant_sku).first()
            if not user_variant_obj:
                raise ValidationError(code="order_item", message={
                    "items": "Invalid order item with sku {} when processing fulfillment order".format(
                        variant_sku)})

            user_variant_id = user_variant_obj.id

            related_item_obj = order_item_obj_dict.get(user_variant_id)
            if not related_item_obj:
                raise ValidationError(code="order_item", message={
                    "items": "Invalid order item with user_variant_id {} when processing fulfillment order".format(
                        user_variant_id)})
            related_item_obj.mfr_base_cost = item_data["base_cost"]
            related_item_obj.save()
            order_item_obj_rejected_flag[user_variant_id] = False
            order_pack_ids.add(related_item_obj.order_pack.id)
        FulfillmentOrderPack.objects.bulk_create(list(
            map(lambda pack_id: FulfillmentOrderPack(order_pack_id=pack_id, mfr_pack_id=mfr_pack_id), order_pack_ids)))
        fulfillment_pack_cost += calculate_fulfillment_order_cost(pack_data)
    updated_packs = set()
    rejected_items = []
    for user_variant_id, is_rejected in order_item_obj_rejected_flag.items():
        if not is_rejected:
            continue
        related_item_obj = order_item_obj_dict[user_variant_id]
        related_item_obj.set_rejected()
        updated_packs.add(related_item_obj.order_pack)
        rejected_items.append(related_item_obj)
    create_order_history_for_fulfill_reject_items(order_obj, rejected_items)
    transaction.on_commit(lambda: update_order_packs_static_fulfill_status(order_obj, updated_pack_objs=updated_packs))
    transaction.on_commit(lambda: update_order_static_financial_status(order_obj))
    transaction.on_commit(lambda: sync_new_packs(order_obj))
    transaction.on_commit(lambda: create_refund_for_rejected_items(order_obj, rejected_item_objs=rejected_items))
    transaction.on_commit(lambda: update_order_cached_metadata_task.delay(order_obj.id))
    sync_paid_order(order_obj)
    # update fulfillment order cost
    try:
        order_id = request_data['id']
        Order.objects.filter(id=order_id).update(
            total_mfr_cost=fulfillment_pack_cost
        )
    except Exception as e:
        logger.error(e)

    def create_order_holding():
        try:
            refund_amount = sum(list(Refund.objects.filter(object_id=order_id).values_list('amount', flat=True)))
            ph_cost = order_obj.total_cost - refund_amount
            if fulfillment_pack_cost > ph_cost:
                try:
                    setting = SystemSetting.objects.get(
                        type=SystemSettingTypes.AUTO_SEND_UNPROFITABLE_ORDER_NOTIFICATION).value
                    if setting.get('auto_send'):
                        recipient = setting.get('recipient', [])
                        send_unprofitable_order_email(order_obj, ph_cost, fulfillment_pack_cost, recipient)
                except Exception as error:
                    logger.info(error)
                OrderHolding.objects.create(
                    order=order_obj,
                    fulfillment_payload=request_data,
                    printholo_cost=ph_cost,
                    fulfillment_cost=fulfillment_pack_cost
                )
        except Exception as e:
            logger.error(e)

    transaction.on_commit(create_order_holding)
    return order_obj


def send_unprofitable_order_email(order_obj, ph_cost, ffm_cost, recipient):
    user = order_obj.shop.owner
    template = Template.objects.get(type=MessageType.UNPROFITABLE_ORDER_NOTIFICATION)
    data = {'order_id': order_obj.id, 'ph_cost': ph_cost, 'ffm_cost': ffm_cost}
    send_html = True
    send_user_email(user, template, data, recipient, send_html)


def sync_new_packs(order_obj):
    AdapterOrderCommunicationService.fulfill_order(order_obj, order_obj.packs.all())


@transaction.atomic
def reject_order(order, request_data):
    packs = order.packs.filter(fulfill_status=OrderPackFulfillStatus.REQUESTED_FULFILLMENT)
    if len(packs) < 0:
        raise ValidationError(code="order", message={"items": "Invalid order"})
    rejected_items = []
    for pack in packs:
        items = pack.items.all()
        items.update(fulfill_status=OrderItemFulfillStatus.REJECTED)
        rejected_items += items
    logger.info(rejected_items)
    transaction.on_commit(lambda: update_order_packs_static_fulfill_status(order, updated_pack_objs=packs))
    transaction.on_commit(lambda: update_order_static_fulfill_status(order))
    transaction.on_commit(lambda: create_refund_for_rejected_items(order, rejected_item_objs=rejected_items))
    transaction.on_commit(lambda: create_order_history_for_fulfill_reject(order, reason=request_data.get("message")))

    try:
        ffm_order_rejected_settings = SystemSetting.objects.get(type=SystemSettingTypes.FFM_SERVICE_SETTING).value.get(
            'order_rejected')
        auto_send = ffm_order_rejected_settings.get('auto_send')
        receive_email_cc = ffm_order_rejected_settings.get('receive_email_cc')
        if auto_send:
            send_admin_notification.delay(message_type=MessageType.ORDER_REJECTED, data={'order_id': order.id},
                                          emails=receive_email_cc)
    except Exception as e:
        logger.exception(e)
    send_notification_task.delay(order.shop.owner_id, MessageType.ORDER_REJECTED, {'order_id': order.id})
    send_notification_task.delay(order.shop.owner_id, MessageType.ORDER_REJECTED_SHOP_OWNER,
                                 {'order_id': order.order_id},
                                 [order.shop.email])
    return order


def sync_paid_order(order_obj):
    FulfillOrderCommunicationService.mark_as_paid(order_obj)


def sync_order_shipping_address(order_obj):
    FulfillOrderCommunicationService.update_shipping_address(order_obj)


def sync_adapter_order(order_obj):
    AdapterOrderCommunicationService.update_order(order_obj)


def scan_to_prepare_to_charge_orders():
    orders = Order.objects.are_item_editable().edit_order_items_delay_was_expired().last_created_earlier_x_min_ago(0)
    for order_obj in orders:
        logger.info(f'Prepare to charge {order_obj.id}')
        prepare_to_charge_order(order_obj)


@transaction.atomic
def prepare_to_charge_order(order_obj):
    if order_obj.fulfill_status != OrderFulfillStatus.UNFULFILLED:
        return
    update_order_cost(order_obj)
    create_order_history_for_is_item_editable_change(order_obj, True, False)
    for pack in order_obj.packs.unfulfilled():
        InvoiceService.create_new_fulfillment_invoice_pack(pack)
        pack.set_fulfill_status(OrderPackFulfillStatus.PENDING)
    order_obj.fulfill_status = OrderFulfillStatus.PENDING
    order_obj.save()


def scan_to_push_orders_to_fulfill():
    orders = Order.objects.filter(fulfill_status=OrderFulfillStatus.PENDING,
                                  financial_status=OrderFinancialStatus.PAID)
    for order_obj in orders:
        push_order_to_fulfill(order_obj)


@transaction.atomic
def push_order_to_fulfill(order):
    FulfillOrderCommunicationService.push_order(order)
    push_order_artworks(order)
    order.fulfill_status = OrderFulfillStatus.REQUESTED_FULFILLMENT
    order.packs.pending().update(fulfill_status=OrderPackFulfillStatus.REQUESTED_FULFILLMENT)
    order.save(update_fields=['fulfill_status'])


def push_order_artworks(order_obj):
    shop = order_obj.shop
    user_product_ids = set()
    for order_item in order_obj.items.all():
        user_product_ids.add(order_item.user_variant.user_product_id)
    user_product_artworks = UserProductArtworkFusion.objects.send_to_fulfill_filter().filter(
        user_product__id__in=list(user_product_ids))
    for user_product_artwork in user_product_artworks:
        sync_artwork_by_shop(user_product_artwork, shop)


@task(name=CeleryTask.TASK_UPDATE_ORDER_SUPPORT_TICKET_INFO)
def task_update_order_support_ticket_info(ticket_id):
    orders = Order.objects.filter(support_ticket_targets__ticket__id=ticket_id)
    for order in orders:
        order.unresolved_support_ticket_count = order.support_ticket_targets.exclude(
            ticket__status=SupportTicketStatus.RESOLVED).count()
        order.support_ticket_count = order.support_ticket_targets.count()
        order.save(update_fields=['unresolved_support_ticket_count', 'support_ticket_count'])


def calculate_fulfillment_order_cost(fulfill_pack_data):
    shipping_cost = float(fulfill_pack_data['shipping_cost'])
    item_cost_list = [float(x['total_cost']) for x in fulfill_pack_data['items']]
    total_item_cost = sum(item_cost_list)
    return shipping_cost + total_item_cost


class OrderExistedException(Exception):
    pass


class OrderItemInvalidException(Exception):
    pass
