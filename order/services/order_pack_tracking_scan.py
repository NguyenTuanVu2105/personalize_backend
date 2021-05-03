import logging
from datetime import timedelta

from django.utils import timezone

from HUB.settings import CHECK_TRACKING_STATUS_IF_NOT_UPDATE_IN_MINUTE, CHECK_UNKNOWN_TRACKING_STATUS_IN_MINUTE
from admin_tools.constants import SystemSettingTypes
from admin_tools.models import SystemSetting
from order.constants.fulfill_statuses import ORDER_PACK_STATUSES_HAS_TRACKING
from order.constants.fulfillment_tracking_statuses import FULFILLMENT_ORDER_PACK_TRACKING_STATUSES_NEED_TO_UPDATE, \
    FULFILLMENT_ORDER_PACK_TRACKING_STATUS_VERBOSE_DICT, FulfilmentOrderPackTrackingStatus
from order.forms import FulfillmentOrderPackTrackingForm
from order.models import FulfillmentOrderPack, OrderTracker
from order.services.user_order import update_order_cached_metadata_task
from order.tasks import create_order_delivered_notification_task
from service_communication.services.fulfill_tracking_service import FulfillTrackingService
from service_communication.services.tracking_service import TrackingService

logger = logging.getLogger(__name__)


def check_all_order_pack_tracking():
    setting = SystemSetting.objects.filter(type=SystemSettingTypes.SCHEDULE_UPDATE_TRACKER).first().value
    if setting["turn_on_schedule_update_tracker"]:
        logger.info("check")
        time = timezone.now() - timedelta(minutes=CHECK_TRACKING_STATUS_IF_NOT_UPDATE_IN_MINUTE)
        fulfillment_order_packs = FulfillmentOrderPack.objects.filter(manually_update=False,
                                                                      tracking_status__in=FULFILLMENT_ORDER_PACK_TRACKING_STATUSES_NEED_TO_UPDATE,
                                                                      order_pack__fulfill_status__in=ORDER_PACK_STATUSES_HAS_TRACKING,
                                                                      update_time__lt=time)[:10]
        for fulfillment_order_pack_obj in fulfillment_order_packs:
            logger.info("Checking tracking of " + str(fulfillment_order_pack_obj.id))
            status, carrier, tracking_url = FulfillTrackingService.get_tracking(
                fulfillment_order_pack_obj.tracking_number, fulfillment_order_pack_obj.tracking_company)
            if not status == FulfilmentOrderPackTrackingStatus.UNKNOWN:
                update_order_pack_tracking(fulfillment_order_pack_obj=fulfillment_order_pack_obj,
                                           status=status if not status == FulfilmentOrderPackTrackingStatus.UNKNOWN else fulfillment_order_pack_obj.status,
                                           carrier=carrier,
                                           tracking_url=tracking_url)
            else:
                fulfillment_order_pack_obj.update_time = timezone.now()
                fulfillment_order_pack_obj.save()
            logger.info("Checking tracking of order pack" + str(fulfillment_order_pack_obj.id) + " SUCCESS")


def check_all_unknown_tracking():
    setting = SystemSetting.objects.filter(type=SystemSettingTypes.SCHEDULE_UPDATE_TRACKER).first().value
    if setting["turn_on_schedule_update_tracker"]:
        time = timezone.now() - timedelta(minutes=CHECK_UNKNOWN_TRACKING_STATUS_IN_MINUTE)
        fulfillment_order_packs = FulfillmentOrderPack.objects.filter(manually_update=False,
                                                                      tracking_status__in=[FulfilmentOrderPackTrackingStatus.UNKNOWN],
                                                                      order_pack__fulfill_status__in=ORDER_PACK_STATUSES_HAS_TRACKING,
                                                                      update_time__lt=time)

        for fulfillment_order_pack_obj in fulfillment_order_packs:
            logger.info("Recheck unknown tracking of " + str(fulfillment_order_pack_obj.id))
            try:
                tracking_status, carrier, tracking_url = FulfillTrackingService.get_tracking(fulfillment_order_pack_obj.tracking_number)
                if tracking_url and not tracking_status == FulfilmentOrderPackTrackingStatus.UNKNOWN:
                    update_order_pack_tracking(fulfillment_order_pack_obj=fulfillment_order_pack_obj,
                                               status=tracking_status,
                                               carrier=carrier,
                                               tracking_url=tracking_url)
                    logger.info("Checked unknown tracking of order pack" + str(fulfillment_order_pack_obj.id) + " SUCCESS")
                    continue
            except Exception as e:
                logger.exception(e)
            # because query depend on update time, so we should update here
            fulfillment_order_pack_obj.save()


def update_order_pack_tracking(fulfillment_order_pack_obj, status, carrier, tracking_url):
    order_pack_form = FulfillmentOrderPackTrackingForm(instance=fulfillment_order_pack_obj, data={
        "tracking_status": status,
        "tracking_company": carrier,
        "tracking_url": tracking_url,
    })
    order_pack_form.validate()
    order_pack = order_pack_form.save()
    if status == FulfilmentOrderPackTrackingStatus.DELIVERED:
        create_order_delivered_notification_task.delay(order_id=fulfillment_order_pack_obj.order_pack.order.id)
    update_order_cached_metadata_task.delay(order_pack.order_pack.order_id)