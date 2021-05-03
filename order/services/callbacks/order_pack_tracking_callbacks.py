import logging

from order.models import OrderPack
from order.services.order_pack_tracking import sync_packs_tracking, sync_completed_fulfillment_packs
from service_communication.constants.request_type import RequestType
from service_communication.services.webhook_job_services import WebhookJobRecoveryService

logger = logging.getLogger(__name__)

# ------------------------------------

update_tracking_request_type = RequestType.ADAPTER_UPDATE_TRACKING


def build_sync_pack_from_order_id_and_pack_ids_function(function):
    def get_objs_and_pass_to_function(order_id, pack_ids):
        order_pack_objs = OrderPack.objects.select_related("order").filter(order_id=order_id, id__in=pack_ids)
        if len(order_pack_objs) > 0:
            function(order_pack_objs[0].order, order_pack_objs)

    return get_objs_and_pass_to_function


sync_packs_tracking_from_order_id_and_pack_ids = build_sync_pack_from_order_id_and_pack_ids_function(
    sync_packs_tracking)

WebhookJobRecoveryService.register_function(request_type=update_tracking_request_type,
                                            function=sync_packs_tracking_from_order_id_and_pack_ids)

# ------------------------------------

sync_completed_fulfillment_packs_from_order_id_and_pack_ids = build_sync_pack_from_order_id_and_pack_ids_function(
    sync_completed_fulfillment_packs)

complete_fulfill_request_type = RequestType.ADAPTER_COMPLETE_FULFILL
WebhookJobRecoveryService.register_function(request_type=complete_fulfill_request_type,
                                            function=sync_completed_fulfillment_packs_from_order_id_and_pack_ids)
