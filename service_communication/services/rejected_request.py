import logging

from django.db import transaction

from HUB.exceptions.FormValidationError import FormValidationError
from order.services.service_order import reject_order
from service_communication.constants.rejected_request_statuses import RejectedRequestStatus
from service_communication.constants.request_type import RequestType
from service_communication.models import RejectedRequest


def save_rejected_request(relate_object, request_type, detail):
    logger = logging.getLogger(__name__)
    rejected_request = RejectedRequest.objects.create(relate_object=relate_object,
                                                      request_type=request_type,
                                                      status=RejectedRequestStatus.PENDING,
                                                      detail=detail
                                                      )
    logger.exception(f'Fulfillment rejected request: {rejected_request.id}')


@transaction.atomic
def resolve_rejected_request(user, rejected_request, request_data):
    if rejected_request.status != RejectedRequestStatus.PENDING:
        raise FormValidationError(field="status", code="invalid")

    handle_resolved_request_by_request_type(rejected_request)

    rejected_request.status = RejectedRequestStatus.RESOLVED
    rejected_request.last_update_user = user
    rejected_request.note = request_data.get("note")
    rejected_request.save()


@transaction.atomic
def confirm_rejected_request(user, rejected_request, request_data):
    if rejected_request.status != RejectedRequestStatus.PENDING:
        raise FormValidationError(field="status", code="invalid")

    handle_confirm_rejected_request_by_type(rejected_request)

    rejected_request.status = RejectedRequestStatus.REJECTED
    rejected_request.last_update_user = user
    rejected_request.note = request_data.get("note")
    rejected_request.save()


def handle_confirm_rejected_request_by_type(rejected_request):
    request_type = rejected_request.request_type
    if request_type == RequestType.FULFILL_PUSH_ORDER:
        reject_order(rejected_request.relate_object, rejected_request.detail)


def handle_resolved_request_by_request_type(rejected_request):
    pass
