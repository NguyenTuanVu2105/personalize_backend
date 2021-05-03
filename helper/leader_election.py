import json
import logging
import os

import requests

from HUB import settings

logger = logging.getLogger(__name__)
MY_POD_NAME = os.environ.get("MY_POD_NAME")


def is_master():
    if settings.LEADER_ELECTION_ENDPOINT is not None:
        try:
            res = requests.get(settings.LEADER_ELECTION_ENDPOINT)
            master_name = json.loads(res.text)['name']
            return MY_POD_NAME == master_name
        except Exception as e:
            logger.exception(e)
            return False
    else:
        return True
