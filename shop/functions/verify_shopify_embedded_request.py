import hashlib
import hmac
import logging
import traceback
import urllib
from datetime import datetime

from django.conf import settings

logger = logging.getLogger(__name__)
SECRET_KEY = settings.SHOPIFY_API_SECRET_KEY
EMBEDDED_REQUEST_TIMEOUT = settings.EMBEDDED_REQUEST_TIMEOUT


def verify_shopify_embedded_request(query_params):
    try:
        cleaned_params = []
        hmac_value = dict(query_params)['hmac']
        timestamp = dict(query_params)['timestamp']

        for (k, v) in sorted(query_params):
            if k in ['hmac', 'signature']:
                continue
            cleaned_params.append((k, v))

        new_qs = urllib.parse.urlencode(cleaned_params, safe=":/")
        secret = SECRET_KEY.encode("utf8")
        h = hmac.new(secret, msg=new_qs.encode("utf8"), digestmod=hashlib.sha256)

        request_time = datetime.fromtimestamp(int(timestamp))
        now = datetime.now()
        sub = (now - request_time).total_seconds()

        logger.info(h.hexdigest())
        logger.info(hmac_value)

        return hmac.compare_digest(h.hexdigest(), hmac_value) and sub < EMBEDDED_REQUEST_TIMEOUT

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
        return False
