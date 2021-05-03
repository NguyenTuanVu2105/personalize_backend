import logging

from django.db import transaction

from order.constants.fulfill_statuses import OrderPackFulfillStatus
from order.models import OrderPack, Order
from order.services.order_status import update_order_static_fulfill_status
from order.services.service_order import sync_new_packs, sync_adapter_order, \
    sync_order_shipping_address, push_order_to_fulfill, sync_paid_order
from service_communication.constants.request_type import RequestType
from service_communication.services.rejected_request import save_rejected_request
from service_communication.services.webhook_job_services import WebhookJobCallbackService, WebhookJobRecoveryService
from .order_pack_tracking_callbacks import build_sync_pack_from_order_id_and_pack_ids_function

logger = logging.getLogger(__name__)

# ------------------------------------
fulfill_order_request_type = RequestType.ADAPTER_FULFILL_ORDER

sync_new_packs_from_order_id_and_pack_ids = build_sync_pack_from_order_id_and_pack_ids_function(sync_new_packs)


@transaction.atomic
def process_order_successful_callback(order, resp_data):
    fulfilled_packs = resp_data["fulfillments"]
    for pack in fulfilled_packs:
        OrderPack.objects.filter(pk=pack["id"]).update(merch_pack_id=pack["fulfill_id"])


def process_order_failed_callback(order, resp_data):
    logger.warning("Failed to process order {}".format(order.id))


WebhookJobCallbackService.register_callbacks(request_type=fulfill_order_request_type,
                                             callbacks=(process_order_successful_callback,
                                                        process_order_failed_callback))

WebhookJobRecoveryService.register_function(request_type=fulfill_order_request_type,
                                            function=sync_new_packs_from_order_id_and_pack_ids)

# ------------------------------------


mark_as_paid_request_type = RequestType.FULFILL_MARK_AS_PAID


def build_sync_order_from_order_id_function(function):
    def get_objs_and_pass_to_function(order_id):
        order_obj = Order.objects.filter(id=order_id).first()
        if order_obj:
            function(order_obj)

    return get_objs_and_pass_to_function


sync_paid_order_from_order_id = build_sync_order_from_order_id_function(sync_paid_order)


def mark_as_paid_order_successful_callback(order_obj, response):
    order_obj.packs.requested_fulfillment().update(fulfill_status=OrderPackFulfillStatus.IN_PRODUCTION)
    update_order_static_fulfill_status(order_obj)


def mark_as_paid_order_failed_callback(order_obj, response):
    pass


WebhookJobCallbackService.register_callbacks(request_type=mark_as_paid_request_type,
                                             callbacks=(mark_as_paid_order_successful_callback,
                                                        mark_as_paid_order_failed_callback))

WebhookJobRecoveryService.register_function(request_type=mark_as_paid_request_type,
                                            function=sync_paid_order_from_order_id)

# ------------------------------------

sync_order_shipping_address_from_order_id = build_sync_order_from_order_id_function(sync_order_shipping_address)

WebhookJobRecoveryService.register_function(request_type=RequestType.FULFILL_UPDATE_SHIPPING_ADDRESS,
                                            function=sync_order_shipping_address_from_order_id)

# ------------------------------------

sync_adapter_order_from_order_id = build_sync_order_from_order_id_function(sync_adapter_order)

WebhookJobRecoveryService.register_function(request_type=RequestType.ADAPTER_UPDATE_ORDER,
                                            function=sync_adapter_order_from_order_id)

# ------------------------------------
push_order_request_type = RequestType.FULFILL_PUSH_ORDER

push_new_order_from_order_id = build_sync_order_from_order_id_function(push_order_to_fulfill)


def push_order_request_success_callback(order, resp_data):
    if not resp_data.get('success', False):
        save_rejected_request(order, push_order_request_type, resp_data)


def push_order_request_failed_callback(order, resp_data):
    save_rejected_request(order, push_order_request_type, resp_data)


WebhookJobRecoveryService.register_function(request_type=push_order_request_type,
                                            function=push_new_order_from_order_id)

WebhookJobCallbackService.register_callbacks(request_type=push_order_request_type,
                                             callbacks=(push_order_request_success_callback,
                                                        push_order_request_failed_callback))
