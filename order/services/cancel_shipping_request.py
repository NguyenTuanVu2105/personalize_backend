import logging

from django.core.exceptions import ValidationError
from django.db import transaction

from order.constants.cancel_shipping_request_statuses import CancelShippingRequestStatus
from order.constants.fulfill_statuses import OrderPackFulfillStatus
from order.forms import CancelShippingRequestCreationForm

logger = logging.getLogger(__name__)


@transaction.atomic
def create_cancel_shipping_request(owner, order, order_pack_ids):
    if not order_pack_ids:
        raise ValidationError(code="packs", message={"packs": "packs field must be nonempty array"})
    order_packs = order.packs.filter(pk__in=order_pack_ids,
                                     fulfill_status=OrderPackFulfillStatus.IN_PRODUCTION,
                                     order__shop__owner=owner) \
        .exclude(cancel_shipping_requests__status__in=[CancelShippingRequestStatus.PENDING, CancelShippingRequestStatus.APPROVED])
    if order_packs.count() != len(order_pack_ids):
        raise ValidationError(code="packs", message={"packs": "Some order_pack_ids is invalid"})
    form = CancelShippingRequestCreationForm({"user": owner.id, "order_packs": order_packs, "order": order.id})
    if form.is_valid():
        form.save()
    else:
        raise ValidationError(code="cancel_shipping_request", message=form.errors)
