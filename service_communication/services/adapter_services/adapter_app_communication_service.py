import logging

from service_communication.constants.request_method import RequestMethod
from service_communication.constants.request_type import RequestType
from service_communication.constants.webhook_job_queue_ids import WebhookJobQueueID
from service_communication.services.webhook_job_services import WebhookJobService
from shop.serializers import MerchantServiceShopSerializer
from .adapter_base_communication_service import AdapterBaseCommunicationService

logger = logging.getLogger(__name__)


class AdapterAppCommunicationService(AdapterBaseCommunicationService):
    HOST = AdapterBaseCommunicationService.HOST
    ENDPOINTS = {
        RequestType.ADAPTER_INIT_APP: "{}/app/hub/init".format(HOST),
        RequestType.ADAPTER_UNINSTALL_APP: "{}/app/hub/uninstall".format(HOST),
        RequestType.ADAPTER_POST_INIT_APP: "{}/app/hub/post-init".format(HOST),
        RequestType.ADAPTER_CREATE_CUSTOMIZE_PAGE: "{}/page/hub/create".format(HOST)
    }
    webhook_job_service = WebhookJobService(queue_id=WebhookJobQueueID.ADAPTER_APP)

    @classmethod
    def uninstall_app(cls, shop):
        shop_info = MerchantServiceShopSerializer(shop).data
        request_type = RequestType.ADAPTER_UNINSTALL_APP
        resp = cls.request_and_log(request_type, shop, RequestMethod.POST, cls.ENDPOINTS[request_type], shop_info, {})
        return resp.json()

    @classmethod
    def init_app(cls, shop):
        req_data = MerchantServiceShopSerializer(shop).data
        request_type = RequestType.ADAPTER_INIT_APP
        resp = cls.request_and_log(request_type, shop, RequestMethod.POST, cls.ENDPOINTS[request_type], req_data, {})
        return resp.json()

    @classmethod
    def post_init_app(cls, shop):
        req_data = MerchantServiceShopSerializer(shop).data
        request_type = RequestType.ADAPTER_POST_INIT_APP
        cls.create_request_job(request_type=request_type, relate_object=shop,
                               relate_params={"shop_id": shop.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type],
                               data=req_data,
                               headers={})

    @classmethod
    def create_customize_page(cls, shop):
        req_data = MerchantServiceShopSerializer(shop).data
        request_type = RequestType.ADAPTER_CREATE_CUSTOMIZE_PAGE
        resp = cls.request_and_log(request_type, shop, RequestMethod.POST, cls.ENDPOINTS[request_type], req_data, {})
        return resp.json()