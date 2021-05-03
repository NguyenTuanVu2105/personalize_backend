import logging

from HUB.settings import LIMIT_GET_ECOMERCE_PRODUCT
from service_communication.constants.request_method import RequestMethod
from service_communication.constants.request_type import RequestType
from shop.serializers import MerchantServiceShopSerializer
from service_communication.services.webhook_job_services import WebhookJobService
from .adapter_base_communication_service import AdapterBaseCommunicationService
from service_communication.constants.webhook_job_queue_ids import WebhookJobQueueID

logger = logging.getLogger(__name__)


class AdapterProductCommunicationService(AdapterBaseCommunicationService):
    HOST = AdapterBaseCommunicationService.HOST
    ENDPOINTS = {
        RequestType.ADAPTER_ADD_NEW_PRODUCT: "{}/product/hub/new".format(HOST),
        RequestType.ADAPTER_UPDATE_PRODUCT: "{}/product/hub/update/{{}}".format(HOST),
        RequestType.ADAPTER_DELETE_PRODUCT: "{}/product/hub/delete/{{}}".format(HOST),
        RequestType.ADAPTER_GET_PRODUCT: "{}/product/hub".format(HOST)
    }

    webhook_job_service = WebhookJobService(queue_id=WebhookJobQueueID.ADAPTER_PRODUCT)

    @classmethod
    def get_product(cls, shop, since_id=None):
        shop_info = MerchantServiceShopSerializer(shop).data
        shop_info['since_id'] = since_id
        shop_info['limit'] = LIMIT_GET_ECOMERCE_PRODUCT
        request_type = RequestType.ADAPTER_GET_PRODUCT
        resp = cls.request_and_log(request_type, shop, RequestMethod.GET, cls.ENDPOINTS[request_type], shop_info, {})
        return resp.json()

    @classmethod
    def new_product(cls, shop_user_product, data):
        request_type = RequestType.ADAPTER_ADD_NEW_PRODUCT
        cls.create_request_job(request_type=request_type, relate_object=shop_user_product,
                               relate_params={"shop_user_product_id": shop_user_product.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type],
                               data=data,
                               headers={})

    @classmethod
    def update_product(cls, shop_user_product, data):
        request_type = RequestType.ADAPTER_UPDATE_PRODUCT
        cls.create_request_job(request_type=request_type, relate_object=shop_user_product,
                               relate_params={"shop_user_product_id": shop_user_product.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type].format(shop_user_product.product_id),
                               data=data,
                               headers={})

    @classmethod
    def delete_product(cls, shop_user_product, data):
        request_type = RequestType.ADAPTER_DELETE_PRODUCT
        cls.create_request_job(request_type=request_type, relate_object=shop_user_product,
                               relate_params={"shop_user_product_id": shop_user_product.id},
                               method=RequestMethod.DELETE,
                               url=cls.ENDPOINTS[request_type].format(shop_user_product.product_id),
                               data=data,
                               headers={})
