import logging

from billing.constants.transaction_statuses import TransactionStatus
from billing.sub_apps.paypal_payment.services.paypal_endpoint_service import PaypalEndpointService
from billing.sub_apps.paypal_payment.services.paypal_request_services import PaypalRequestService

logger = logging.getLogger(__name__)


class PaypalOrderService:
    @classmethod
    def create_order_for_authorize(cls):
        response_json = PaypalRequestService.post(url=PaypalEndpointService.CHECKOUT_ORDER,
                                                  data={
                                                      "intent": "CAPTURE",
                                                      "purchase_units": [
                                                          {
                                                              "amount": {
                                                                  "currency_code": "USD",
                                                                  "value": "0.01"
                                                              }
                                                          }
                                                      ]
                                                  })
        order_id = response_json.get("id", "")
        if not order_id.strip():
            logger.error("Can't create new Paypal vault order\n{}".format(response_json))
            return
        return order_id

    @classmethod
    def capture_order(cls, order_id):
        response_json = PaypalRequestService.post(
            url=PaypalEndpointService.CAPTURE_ORDER.format(order_id=order_id),
            data={})
        order_id = response_json.get("id", "")
        if not order_id.strip():
            logger.error("Can't capture Paypal order [{}]\n{}".format(order_id, response_json))
            return False
        for purchase_units in response_json['purchase_units']:
            if any(capture['final_capture'] and capture['status'] == 'COMPLETED' for capture in
                   purchase_units['payments']['captures']):
                return True
        return False

    @classmethod
    def charge_by_payment_token(cls, invoice_id, idempotency_key, payment_token, amount):
        response_json = PaypalRequestService.post(url=PaypalEndpointService.CHECKOUT_ORDER,
                                                  data={
                                                      "intent": "CAPTURE",
                                                      "payment_source": {
                                                          "token": {
                                                              "id": payment_token,
                                                              "type": "PAYMENT_METHOD_TOKEN"
                                                          }
                                                      },
                                                      "purchase_units": [
                                                          {
                                                              "amount": {
                                                                  "currency_code": "USD",
                                                                  "value": amount
                                                              },
                                                              "description": f'Invoice {invoice_id}',
                                                              "invoice_id": invoice_id
                                                          }

                                                      ]
                                                  },
                                                  idempotency_key=idempotency_key)

        status = cls.handle_order_transaction_detail(response_json)
        return status, response_json

    @classmethod
    def get_order_detail(cls, capture_id):
        response_json = PaypalRequestService.get(
            url=PaypalEndpointService.GET_CAPTURE_DETAIL.format(capture_id=capture_id),
            data={})
        order_transaction_detail = cls.rebuild_order_transaction_detail(capture_transaction_detail=response_json)
        status = cls.handle_order_transaction_detail(order_transaction_detail)
        return status, order_transaction_detail

    @classmethod
    def rebuild_order_transaction_detail(cls, capture_transaction_detail, **kwargs):
        return {
            **kwargs,
            "id": None,
            "links": [],
            "status": "COMPLETED",
            "intent": "capture",
            "purchase_units": [
                {
                    "payments": {
                        "captures": [capture_transaction_detail]
                    }
                },
            ]
        }

    @classmethod
    def handle_order_transaction_detail(cls, response_json):
        status = TransactionStatus.CHARGE_FAILED
        paypal_order_status = response_json.get("status")
        if paypal_order_status == "COMPLETED":
            purchase_units = response_json.get("purchase_units", [])
            if len(purchase_units):
                related_captures = purchase_units[0].get("payments", {}).get("captures")
                if len(related_captures):
                    related_captures = related_captures[0]
                    capture_status = related_captures.get("status")
                    if capture_status == "COMPLETED":
                        status = TransactionStatus.SUCCESS
                    elif capture_status in ("DECLINED", "PARTIALLY_REFUNDED", "REFUNDED"):
                        status = TransactionStatus.CHARGE_FAILED
                    elif capture_status == "PENDING":
                        status = TransactionStatus.TRANSACTION_PENDING
        elif paypal_order_status in ("CREATED", "SAVED", "APPROVED"):
            status = TransactionStatus.TRANSACTION_PENDING
        else:
            status = TransactionStatus.CHARGE_FAILED
        return status

    @classmethod
    def get_transaction_id(cls, transaction_detail):
        return transaction_detail.get("purchase_units", [{}])[0].get("payments", {}).get("captures", [{}])[0].get("id")


def paypal_vault_auto_charge(invoice, paypal_vault_payment_method, idempotency_key):
    status, detail = PaypalOrderService.charge_by_payment_token(invoice.payment_gateway_invoice_id,
                                                                idempotency_key,
                                                                paypal_vault_payment_method.payment_token,
                                                                invoice.total_cost)
    return status, detail
