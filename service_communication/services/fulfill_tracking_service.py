import os

from HUB.settings.tracking_setting import FULFILL_TRACKING_URL, FULFILL_TRACKING_API_KEY
import requests
import logging

from order.constants.fulfillment_tracking_statuses import FULFILLMENT_ORDER_PACK_TRACKING_STATUS_VERBOSE_DICT, \
    FulfilmentOrderPackTrackingStatus
from order.models import OrderTracker

logger = logging.getLogger(__name__)

class FulfillTrackingAPI:
    GET_TRACKING_URL = FULFILL_TRACKING_URL + "/tracking-number/import"

    def __init__(self, api_key):
        self.api_key = api_key

    def _post(self, url, data):
        headers = {
            "x-api-key": self.api_key
        }
        return requests.post(url, data=data, headers=headers)

    def get_tracking(self, tracking_code, carrier=None):
        payloads = {
            "tracking_code": tracking_code,
            "carrier": carrier or "Other"
        }
        return self._post(self.GET_TRACKING_URL, payloads).json()


class FulfillTrackingService:
    tracker = FulfillTrackingAPI(api_key=FULFILL_TRACKING_API_KEY)
    base_tracking_url = os.environ.get("CLIENT_URL") + "/tracking/{}"

    @classmethod
    def get_tracking(cls, tracking_code, carrier=None):
        tracking_resp = cls.tracker.get_tracking(tracking_code, carrier)
        tracking_url = cls.base_tracking_url.format(tracking_code)
        logger.info("Tracking code {}".format(tracking_code))
        logger.info(tracking_resp)
        if tracking_resp["success"]:
            tracker = tracking_resp["data"]
            update_tracking_history(tracking_code, tracker)
            return FULFILLMENT_ORDER_PACK_TRACKING_STATUS_VERBOSE_DICT[tracker["status"]],tracker["carrier"], tracking_url
        else:
            return FulfilmentOrderPackTrackingStatus.UNKNOWN, None, None

def update_tracking_history(tracking_code, tracker):
    try:
        OrderTracker.objects.update_or_create(tracking_code=tracking_code, defaults={"payloads": tracker})
    except Exception as e:
        logger.error(str(e))
