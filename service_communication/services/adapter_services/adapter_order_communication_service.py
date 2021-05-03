import logging

from order.constants.fulfill_statuses import VerboseOrderFulfillStatus
from order.constants.order_types import OrderTypes
from order.serializers import MerchantServiceOrderPackSerializer
from order.serializers.adapter_update_order import AdapterUpdateOrderSerializer
from order.serializers.order_pack import MerchantServicePackTrackingSerializer
from service_communication.constants.request_method import RequestMethod
from service_communication.constants.request_type import RequestType
from service_communication.constants.webhook_job_queue_ids import WebhookJobQueueID
from service_communication.services.webhook_job_services import WebhookJobService
from shop.serializers import MerchantServiceShopSerializer
from .adapter_base_communication_service import AdapterBaseCommunicationService

logger = logging.getLogger(__name__)


class AdapterOrderCommunicationService(AdapterBaseCommunicationService):
    HOST = AdapterBaseCommunicationService.HOST
    ENDPOINTS = {
        RequestType.ADAPTER_FULFILL_ORDER: "{}/order/hub/fulfillment/".format(HOST),
        RequestType.ADAPTER_UPDATE_TRACKING: "{}/order/hub/fulfillment/tracking".format(HOST),
        RequestType.ADAPTER_COMPLETE_FULFILL: "{}/order/hub/fulfillment/complete".format(HOST),
        RequestType.ADAPTER_LIST_ORDER: "{}/order/hub/list_ids_by_update_time".format(HOST),
        RequestType.ADAPTER_LIST_ORDER_BY_IDS: "{}/order/hub/list-by-ids".format(HOST),
        RequestType.ADAPTER_UPDATE_ORDER: "{}/order/hub/update".format(HOST),
        RequestType.ADAPTER_CANCEL_FULFILL: "{}/order/hub/fulfillment/cancel".format(HOST),
        RequestType.ADAPTER_GET_SHIPPING_RATE: "{}/carrier/hub/shipping-zones/".format(HOST),
    }

    webhook_job_service = WebhookJobService(queue_id=WebhookJobQueueID.ADAPTER_ORDER)

    @classmethod
    def order_illegal_request_to_adapter(cls, order):
        return order.type == OrderTypes.PRINTHOLO or order.shop.is_default_printholo_shop()

    @classmethod
    def fulfill_order(cls, order, new_packs):
        new_pack_data = MerchantServiceOrderPackSerializer(new_packs, many=True).data
        new_pack_data = [x for x in new_pack_data if x['fulfill_status'] != VerboseOrderFulfillStatus.REJECTED]
        if len(new_pack_data) == 0 or cls.order_illegal_request_to_adapter(order):
            return
        fulfill_data = {"fulfillments": new_pack_data}
        request_data = cls.prepare_request_body(order, fulfill_data)
        request_type = RequestType.ADAPTER_FULFILL_ORDER
        cls.create_request_job(request_type=request_type, relate_object=order,
                               relate_params={"order_id": order.id, "pack_ids": [pack.id for pack in new_packs]},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type],
                               data=request_data,
                               headers={})

    @classmethod
    def update_order(cls, order):
        if cls.order_illegal_request_to_adapter(order):
            return
        data = AdapterUpdateOrderSerializer(instance=order).data
        request_data = cls.prepare_request_body(order, data)
        cls.create_request_job(request_type=RequestType.ADAPTER_UPDATE_ORDER, relate_object=order,
                               relate_params={"order_id": order.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[RequestType.ADAPTER_UPDATE_ORDER],
                               data=request_data,
                               headers={})

    @classmethod
    def update_packs(cls, order, updated_packs, handler):
        if cls.order_illegal_request_to_adapter(order):
            return
        updated_packs = cls.filter_invalid_ecommerce_packs(updated_packs)
        if len(updated_packs) == 0:
            logger.warning("No pack valid to update")
            return
        updated_packs_data = MerchantServicePackTrackingSerializer(updated_packs, many=True).data
        tracking_data = {"fulfillments": updated_packs_data}
        request_data = cls.prepare_request_body(order, tracking_data)
        handler(order, updated_packs, request_data)

    @classmethod
    def update_tracking(cls, order, updated_packs, request_data):
        request_type = RequestType.ADAPTER_UPDATE_TRACKING
        cls.create_request_job(request_type=request_type, relate_object=order,
                               relate_params={"order_id": order.id, "pack_ids": [pack.id for pack in updated_packs]},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type],
                               data=request_data,
                               headers={})

    @classmethod
    def complete_fulfill(cls, order, updated_packs, request_data):
        request_type = RequestType.ADAPTER_COMPLETE_FULFILL
        cls.create_request_job(request_type=request_type, relate_object=order,
                               relate_params={"order_id": order.id, "pack_ids": [pack.id for pack in updated_packs]},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type],
                               data=request_data,
                               headers={})

    @classmethod
    def cancel_fulfill(cls, order, updated_packs, request_data):
        request_type = RequestType.ADAPTER_CANCEL_FULFILL
        cls.create_request_job(request_type=request_type, relate_object=order,
                               relate_params={"order_id": order.id, "pack_ids": [pack.id for pack in updated_packs]},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type],
                               data=request_data,
                               headers={})

    @classmethod
    def get_order_by_update_time(cls, shop):
        shop_info = MerchantServiceShopSerializer(shop).data
        shop_info["lastUpdate"] = str(shop.order_scan_info.last_order_update_time.isoformat())
        request_type = RequestType.ADAPTER_LIST_ORDER
        resp = cls.request_and_log(request_type, shop, RequestMethod.GET, cls.ENDPOINTS[request_type], shop_info, {})
        return resp.json()

    @classmethod
    def get_list_order_by_id(cls, shop, ids):
        shop_info = MerchantServiceShopSerializer(shop).data
        shop_info["ids"] = ids
        request_type = RequestType.ADAPTER_LIST_ORDER_BY_IDS
        resp = cls.request_and_log(request_type, shop, RequestMethod.GET, cls.ENDPOINTS[request_type], shop_info, {})
        return resp.json()

    @classmethod
    def get_shipping_rates(cls, shop):
        shop_info = MerchantServiceShopSerializer(shop).data
        request_type = RequestType.ADAPTER_GET_SHIPPING_RATE
        resp = cls.request_and_log(request_type, shop, RequestMethod.GET, cls.ENDPOINTS[request_type], shop_info, {})
        return resp.json()

    @classmethod
    def prepare_request_body(cls, order, data):
        shop_info = MerchantServiceShopSerializer(order.shop).data
        return {
            **shop_info,
            "data": {"id": order.order_id, **data}
        }

    @classmethod
    def filter_invalid_ecommerce_packs(cls, packs):
        return [pack for pack in packs if pack.merch_pack_id is not None]
