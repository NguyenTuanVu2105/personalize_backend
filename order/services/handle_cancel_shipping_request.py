from django.core.exceptions import ValidationError
from django.db import transaction

from billing.forms import CancelShippingRefundCreationForm
from notification.enums.message_types import MessageType
from notification.services.notification import send_notification_task
from order.constants.cancel_shipping_request_statuses import CancelShippingRequestStatus
from order.constants.fulfill_statuses import OrderPackFulfillStatus
from order.forms import CancelShippingRequestHandleForm
from order.services.order_status import update_order_static_fulfill_status


@transaction.atomic
def approve_cancel_shipping_request(actor, cancel_shipping_request, request_data):
    cancel_shipping_request_approve_form = CancelShippingRequestHandleForm(instance=cancel_shipping_request, data={
        "status": CancelShippingRequestStatus.APPROVED,
        "admin": actor.pk,
        "admin_note": request_data.get("note")})
    if cancel_shipping_request_approve_form.is_valid():
        cancel_shipping_request_approve_form.save()
    else:
        raise ValidationError(code="cancel_shipping_request", message=cancel_shipping_request_approve_form.errors)

    cancel_shipping_request.order_packs.update(fulfill_status=OrderPackFulfillStatus.CANCELED_SHIPPING)
    update_order_static_fulfill_status(cancel_shipping_request.order)

    order_packs = cancel_shipping_request.order_packs.all()
    for order_pack in order_packs:
        invoice_pack = order_pack.invoice_pack
        refund_form = CancelShippingRefundCreationForm(
            {"user": cancel_shipping_request.user.pk, "amount": invoice_pack.shipping_cost,
             "cancel_shipping_request": cancel_shipping_request, "invoice": invoice_pack.invoice.pk})
        if refund_form.is_valid():
            refund_form.save()
        else:
            raise ValidationError(code="refund", message=refund_form.errors)

    notification_data = {
        'order_id': order_packs[0].order.id
    }
    send_notification_task.delay(cancel_shipping_request.user.id, MessageType.CANCEL_SHIPPING_APPROVED, notification_data)


@transaction.atomic
def reject_cancel_shipping_request(actor, cancel_shipping_request, request_data):
    cancel_shipping_request_approve_form = CancelShippingRequestHandleForm(instance=cancel_shipping_request, data={
        "status": CancelShippingRequestStatus.REJECTED,
        "admin": actor.pk,
        "admin_note": request_data.get("note")})
    if cancel_shipping_request_approve_form.is_valid():
        cancel_shipping_request_approve_form.save()
    else:
        raise ValidationError(code="cancel_shipping_request", message=cancel_shipping_request_approve_form.errors)

    notification_data = {
        'order_id': cancel_shipping_request.order_packs.all()[0].order.id
    }
    send_notification_task.delay(cancel_shipping_request.user.id, MessageType.CANCEL_SHIPPING_REJECTED, notification_data)
