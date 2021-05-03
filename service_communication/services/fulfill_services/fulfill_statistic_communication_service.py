import logging

from service_communication.constants.request_method import RequestMethod
from service_communication.constants.request_type import RequestType
from service_communication.services.webhook_job_services import WebhookJobService
from .fulfill_base_communication_service import FulfillBaseCommunicationService
from service_communication.constants.webhook_job_queue_ids import WebhookJobQueueID

logger = logging.getLogger(__name__)


class FulfillStatisticCommunicationService(FulfillBaseCommunicationService):
    ENDPOINTS = {
        RequestType.FULFILL_PRODUCTION_STATISTICS: "{}/production/statistics".format(
            FulfillBaseCommunicationService.HOST),
        RequestType.FULFILL_SHIPPING_STATISTICS: "{}/shipping-time/statistics".format(
            FulfillBaseCommunicationService.HOST)
    }

    @classmethod
    def get_production_statistic(cls):
        res = cls.request_and_log(request_type=RequestType.FULFILL_PRODUCTION_STATISTICS,
                                  request_object=None,
                                  method=RequestMethod.GET,
                                  url=cls.ENDPOINTS[RequestType.FULFILL_PRODUCTION_STATISTICS],
                                  data={},
                                  headers=cls.HEADERS)
        return res.json()

    @classmethod
    def get_shipping_statistic(cls):
        res = cls.request_and_log(request_type=RequestType.FULFILL_SHIPPING_STATISTICS,
                                  request_object=None,
                                  method=RequestMethod.GET,
                                  url=cls.ENDPOINTS[RequestType.FULFILL_SHIPPING_STATISTICS],
                                  data={},
                                  headers=cls.HEADERS)
        return res.json()
