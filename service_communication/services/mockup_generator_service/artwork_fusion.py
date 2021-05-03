import logging
import os

from service_communication.constants.request_method import RequestMethod
from service_communication.constants.request_type import RequestType
from service_communication.constants.webhook_job_queue_ids import WebhookJobQueueID
from service_communication.services.abstract_service import AbstractCommunicationService
from service_communication.services.webhook_job_services import WebhookJobService

logger = logging.getLogger(__name__)


class MockupArtworkFusionCommunicationService(AbstractCommunicationService):
    FUSION_ARTWORK_GENERATOR_SERVICE = os.environ.get("FUSION_ARTWORK_GENERATOR_SERVICE")
    webhook_job_service = WebhookJobService(queue_id=WebhookJobQueueID.MOCKUP_ARTWORK_FUSION)

    @classmethod
    def generate_artwork_fusion(cls, user_product_artwork_fusion, request_data):
        request_type = RequestType.MOCKUP_GENERATE_ARTWORK_FUSION
        cls.create_request_job(request_type=request_type, relate_object=user_product_artwork_fusion,
                               relate_params={"user_product_artwork_fusion": user_product_artwork_fusion.id},
                               method=RequestMethod.POST,
                               url=cls.FUSION_ARTWORK_GENERATOR_SERVICE,
                               data=request_data,
                               headers={})
