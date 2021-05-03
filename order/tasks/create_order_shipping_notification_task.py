from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from HUB.constants.celery_task import CeleryTask
from notification.services.create_order_tracking_notification import create_order_shipping_notification

logger = get_task_logger(__name__)


@task(name=CeleryTask.TASK_CREATE_ORDER_SHIPPING_NOTIFICATION)
def create_order_shipping_notification_task(order_id):
    """
        Create order shipping notification
    """
    logger.info("create_order_shipping_notification")
    return create_order_shipping_notification(order_id)
