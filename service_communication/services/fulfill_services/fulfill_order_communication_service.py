import logging

from HUB.constants.celery_task import CeleryTask
from abstract_product.models.ffm_product_infos import FFMProductInfo
from admin_tools.constants import SystemSettingTypes
from admin_tools.models import SystemSetting
from order.models.order_mapping_sku_log import OrderMappingSkuLog
from order.serializers import FulfillServiceOrderSerializer
from service_communication.constants.request_method import RequestMethod
from service_communication.constants.request_type import RequestType
from service_communication.services.webhook_job_services import WebhookJobService
from .fulfill_base_communication_service import FulfillBaseCommunicationService
from service_communication.constants.webhook_job_queue_ids import WebhookJobQueueID

logger = logging.getLogger(__name__)


class FulfillOrderCommunicationService(FulfillBaseCommunicationService):
    ENDPOINTS = {
        RequestType.FULFILL_PUSH_ORDER: "{}/orders/{{}}".format(FulfillBaseCommunicationService.HOST),
        RequestType.FULFILL_MARK_AS_PAID: "{}/orders/{{}}/paid".format(FulfillBaseCommunicationService.HOST),
        RequestType.FULFILL_UPDATE_SHIPPING_ADDRESS: "{}/orders/{{}}/address".format(
            FulfillBaseCommunicationService.HOST),
    }

    webhook_job_service = WebhookJobService(queue_id=WebhookJobQueueID.FULFILLMENT_ORDER)

    @classmethod
    def push_order(cls, order):
        request_data = FulfillServiceOrderSerializer(order).data
        request_type = RequestType.FULFILL_PUSH_ORDER
        try:
            if SystemSetting.objects.get(type=SystemSettingTypes.FFM_SERVICE_SETTING) \
                    .value.get('auto_mapping_sku', False):
                for item in request_data['items']:
                    if 'variant' not in item:
                        continue
                    if 'sku' not in item['variant']:
                        continue
                    sku_data = item['variant']['sku']
                    sku = sku_data[:sku_data.index('(') - 1]
                    ffm_product_info = FFMProductInfo.objects.filter(ph_product_sku=sku).first()
                    if ffm_product_info and ffm_product_info.supplier_product_sku != '':
                        item['variant']['sku'] = ffm_product_info.supplier_product_sku
                    else:
                        OrderMappingSkuLog.objects.create(order=order, ph_product_sku=sku,
                                                          note='Cannot find ffm sku')
        except Exception as e:
            logger.info(e)
        cls.create_request_job(request_type=request_type, relate_object=order,
                               relate_params={"order_id": order.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type].format(order.id),
                               data=request_data,
                               headers=cls.HEADERS)

    @classmethod
    def update_shipping_address(cls, order):
        order_data = FulfillServiceOrderSerializer(order).data
        request_data = {"namespace": order.shop.name, "address": order_data.get("address")}
        request_type = RequestType.FULFILL_UPDATE_SHIPPING_ADDRESS
        cls.create_request_job(request_type=request_type, relate_object=order,
                               relate_params={"order_id": order.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type].format(order.id),
                               data=request_data,
                               headers=cls.HEADERS)

    @classmethod
    def mark_as_paid(cls, order):
        request_data = {"namespace": order.shop.name}
        request_type = RequestType.FULFILL_MARK_AS_PAID
        cls.create_request_job(request_type=request_type, relate_object=order,
                               relate_params={"order_id": order.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type].format(order.id),
                               data=request_data,
                               headers=cls.HEADERS)
