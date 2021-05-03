import logging

from service_communication.constants.request_method import RequestMethod
from service_communication.constants.request_type import RequestType
from service_communication.services.webhook_job_services import WebhookJobService
from .fulfill_base_communication_service import FulfillBaseCommunicationService
from service_communication.constants.webhook_job_queue_ids import WebhookJobQueueID

logger = logging.getLogger(__name__)


class FulfillProductCommunicationService(FulfillBaseCommunicationService):
    ENDPOINTS = {
        RequestType.FULFILL_PUSH_ARTWORK: "{}/artworks/{{}}/{{}}".format(FulfillBaseCommunicationService.HOST),
    }
    webhook_job_service = WebhookJobService(queue_id=WebhookJobQueueID.FULFILLMENT_PRODUCT)

    @classmethod
    def push_artwork(cls, user_product_artwork, shop):
        side_data = user_product_artwork.parse_data_for_artwork_pushing()
        product = user_product_artwork.user_product
        cls.create_request_job(request_type=RequestType.FULFILL_PUSH_ARTWORK, relate_object=user_product_artwork,
                               relate_params={"user_product_artwork_id": user_product_artwork.id, "shop_id": shop.id},
                               method=RequestMethod.POST,
                               url=cls.ENDPOINTS[RequestType.FULFILL_PUSH_ARTWORK].format(shop.name, product.id),
                               data=side_data,
                               headers=cls.HEADERS)
