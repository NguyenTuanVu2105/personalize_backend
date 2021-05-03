from service_communication.constants.request_method import RequestMethod
from service_communication.constants.request_type import RequestType
from service_communication.constants.webhook_job_queue_ids import WebhookJobQueueID
from service_communication.services import WebhookJobService
from service_communication.services.adapter_services.adapter_base_communication_service import \
    AdapterBaseCommunicationService
from shop.serializers import MerchantServiceShopSerializer


class AdapterShopCommunicationService(AdapterBaseCommunicationService):
    HOST = AdapterBaseCommunicationService.HOST
    ENDPOINTS = {
        RequestType.ADAPTER_CHECK_SHOP_LOCATION: "{}/shop/hub/check-location".format(HOST),
    }
    webhook_job_service = WebhookJobService(queue_id=WebhookJobQueueID.ADAPTER_SHOP)

    @classmethod
    def check_location(cls, shop):
        req_data = MerchantServiceShopSerializer(shop).data
        request_type = RequestType.ADAPTER_CHECK_SHOP_LOCATION
        cls.create_request_job(request_type=request_type, relate_object=shop,
                               relate_params={"shop_id": shop.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[request_type],
                               data=req_data,
                               headers={})