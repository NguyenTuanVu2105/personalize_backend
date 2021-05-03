import logging

from rest_framework import status
from rest_framework.response import Response

from HUB.views import APIView
from billing.exceptions.invoice_exception import InvoiceDoesNotExist
from billing.exceptions.webhook_exception import InvalidWebhookResourceType
from billing.sub_apps.paypal_payment.services.base.paypal_base_webhook_services import PaypalBaseWebhookService
from service_communication.constants.incoming_webhook_types import IncomingWebhookType
from service_communication.views.generic_incoming_webhook_handle import GenericIncomingWebhookHandle

logger = logging.getLogger(__name__)


class PaypalWebhookView(APIView,
                        GenericIncomingWebhookHandle):
    paypal_webhook_service = PaypalBaseWebhookService
    webhook_type = IncomingWebhookType.PAYPAL_SALE_TRANSACTION_UPDATE

    def post(self, request):
        request_data = request.data

        incoming_webhook = self.save_webhook(webhook_type=self.webhook_type,
                                             request_data=request_data,
                                             meta={
                                                 "headers": dict(request.headers)
                                             })

        self.handle_webhook_error(incoming_webhook, "")
        return Response(status=status.HTTP_404_NOT_FOUND)
