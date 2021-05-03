import logging

import easypost

from HUB import settings
from order.constants.fulfillment_tracking_statuses import FULFILLMENT_ORDER_PACK_TRACKING_STATUS_VERBOSE_DICT
from .abstract_service import AbstractCommunicationService

logger = logging.getLogger(__name__)
easypost.api_key = settings.EASY_POST_API_KEY


class TrackingService(AbstractCommunicationService):

    @classmethod
    def get_tracking(cls, tracking_code, carrier=None):
        tracker = easypost.Tracker.create(
            tracking_code=tracking_code,
            carrier=carrier
        )
        return cls.extract_tracking_info(tracker)

    @classmethod
    def check_tracking_status(cls, tracking_id):
        tracker = easypost.Tracker.retrieve(tracking_id)
        return cls.extract_tracking_info(tracker)

    @classmethod
    def extract_tracking_info(cls, tracker):
        return tracker["id"], FULFILLMENT_ORDER_PACK_TRACKING_STATUS_VERBOSE_DICT[tracker["status"]], tracker["carrier"], tracker["public_url"]
