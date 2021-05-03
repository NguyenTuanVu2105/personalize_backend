from __future__ import absolute_import, unicode_literals

import logging

from HUB.constants.celery_task import CeleryTask
from worker_payment_processor.functions.message_handler import message_handle
from worker_payment_processor.message_subscriber import subscribe

logger = logging.getLogger(__name__)

subscribe(CeleryTask.TASK_CHARGE_INVOICE, message_handle)
