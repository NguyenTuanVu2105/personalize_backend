import logging
import re

from django.core.exceptions import ValidationError
from django.db import transaction

from HUB.exceptions.FormValidationError import FormValidationError
from order.constants.fulfill_statuses import OrderPackFulfillStatus, OrderFulfillStatus
from order.constants.fulfillment_tracking_statuses import FulfilmentOrderPackTrackingStatus
from order.forms.fulfillment_order_pack import FulfillmentOrderPackTrackingForm
from order.models import FulfillmentOrderPack
from order.services.order_status import update_order_static_fulfill_status
from order.services.update_order_delivered import update_order_delivered
from order.services.user_order import update_order_cached_metadata_task
from order.tasks import create_order_delivered_notification_task
from service_communication.services.adapter_services import AdapterOrderCommunicationService
from service_communication.services.fulfill_tracking_service import FulfillTrackingService
from service_communication.services.tracking_service import TrackingService

logger = logging.getLogger(__name__)

@transaction.atomic
def update_order_pack_tracking(order_obj, request_data):
    updated_packs = []
    is_delivered = False
    for pack_data in request_data["fulfillments"]:
        pack_data = standard_pack_request_data(pack_data)
        mfr_pack_id = pack_data["id"]
        fulfillment_pack_objs = FulfillmentOrderPack.objects.select_related("order_pack").filter(
            order_pack__order_id=order_obj.pk, mfr_pack_id=mfr_pack_id)
        if len(fulfillment_pack_objs) <= 0:
            raise FormValidationError(code="invalid", field="pack")
        if pack_data["tracking_company"] not in pack_data or pack_data["tracking_company"] is None:
            status, carrier, tracking_url = FulfillTrackingService.get_tracking(pack_data['tracking_number'])
        else:
            status, carrier, tracking_url = FulfillTrackingService.get_tracking(pack_data['tracking_number'],
                                                                                pack_data["tracking_company"])
        if 'tracking_url' not in pack_data or pack_data['tracking_url'] is None:
            try:
                if tracking_url:
                    pack_data["tracking_status"] = status
                    pack_data["tracking_company"] = carrier
                    pack_data['tracking_url'] = tracking_url
                else:
                    pack_data["tracking_status"] = FulfilmentOrderPackTrackingStatus.UNKNOWN
                    pack_data['tracking_url'] = get_tracking_url(pack_data['tracking_company'],
                                                                 pack_data['tracking_number'])
                # pack_data["tracking_id"] = tracking_id
                is_delivered = is_delivered or status == FulfilmentOrderPackTrackingStatus.DELIVERED
            except Exception as e:
                pack_data["tracking_status"] = FulfilmentOrderPackTrackingStatus.UNKNOWN
                pack_data['tracking_url'] = get_tracking_url(pack_data['tracking_company'],
                                                             pack_data['tracking_number'])
        else:
            try:
                pack_data["tracking_status"] = status
                if "tracking_company" not in pack_data:
                    pack_data["tracking_company"] = carrier or "Other"
            except Exception as e:
                pack_data["tracking_status"] = FulfilmentOrderPackTrackingStatus.UNKNOWN
                pack_data['tracking_url'] = get_other_tracking_url(pack_data['tracking_number'])

        for fulfillment_pack_obj in fulfillment_pack_objs:
            fulfillment_order_pack_form = FulfillmentOrderPackTrackingForm(instance=fulfillment_pack_obj, data=pack_data)
            if fulfillment_order_pack_form.is_valid():
                fulfillment_pack_obj = fulfillment_order_pack_form.save()
                related_order_pack = fulfillment_pack_obj.order_pack
                related_order_pack.set_fulfill_status(OrderPackFulfillStatus.FULFILLED)
                updated_packs.append(related_order_pack)
            else:
                raise ValidationError(code="order", message=fulfillment_order_pack_form.errors)

    transaction.on_commit(lambda: update_order_static_fulfill_status(order_obj))
    transaction.on_commit(lambda: sync_packs_tracking(order_obj, updated_packs))
    transaction.on_commit(lambda: update_order_cached_metadata_task.delay(order_obj.id))
    transaction.on_commit(lambda: sync_completed_fulfillment_packs(order_obj, updated_packs))
    if is_delivered:
        transaction.on_commit(lambda: create_order_delivered_notification_task.delay(order_id=order_obj.id))
        transaction.on_commit(lambda: update_order_delivered(order_id=order_obj.id))
    return order_obj


def standard_pack_request_data(pack_data):
    pack_data['tracking_number'] = re.sub(r'\s+', '', pack_data['tracking_number']) if ('tracking_number' in pack_data and pack_data['tracking_number'] is not None) else None
    pack_data['tracking_url'] = re.sub(r'\s+', '', pack_data['tracking_url']) if ('tracking_url' in pack_data and pack_data['tracking_url'] is not None) else None
    pack_data['origin_tracking_url'] = pack_data['tracking_url']  # original tracking url from FFM
    return pack_data


def sync_packs_tracking(order, updated_packs):
    AdapterOrderCommunicationService.update_packs(order, updated_packs, AdapterOrderCommunicationService.update_tracking)


def sync_completed_fulfillment_packs(order, updated_packs):
    AdapterOrderCommunicationService.update_packs(order, updated_packs, AdapterOrderCommunicationService.complete_fulfill)


def sync_cancelled_fulfillment_packs(order, updated_packs):
    if order.fulfill_status == OrderFulfillStatus.UNFULFILLED:
        logger.info(f'[Cancel Order] Order {order.id} is not fulfilled yet')
        return
    updated_packs = list(filter(lambda pack: pack.merch_pack_id is not None, updated_packs))
    if len(updated_packs) == 0:
        logger.info(f'[Cancel Order] Order {order.id} dont have any fulfillment to update to shopify')
        return
    AdapterOrderCommunicationService.update_packs(order, updated_packs, AdapterOrderCommunicationService.cancel_fulfill)


def get_tracking_url(tracking_company, tracking_number):
    standard_name = tracking_company.lower().replace(" ", "_")
    if standard_name == 'dhl':
        return f'https://webtrack.dhlglobalmail.com/?trackingnumber={tracking_number}'
    elif standard_name == 'usps':
        return f'https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_number}'
    elif standard_name == 'ups':
        return f'https://www.ups.com/track?loc=en_US&tracknum={tracking_number}&requester=NES&agreeTerms=yes/trackdetails'
    elif standard_name == 'sf_express':
        return f'http://www.sf-express.com/us/en/dynamic_function/waybill/#search/bill-number/{tracking_number}'
    else:
        return f'https://t.17track.net/en#nums={tracking_number}'

def get_other_tracking_url(tracking_number):
    return f'https://t.17track.net/en#nums={tracking_number}'