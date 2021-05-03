import logging

from billing.constants.transaction_statuses import TransactionStatus
from .paypal_endpoint_service import PaypalEndpointService
from .paypal_request_services import PaypalRequestService

logger = logging.getLogger(__name__)


class PaypalSaleService:
    @classmethod
    def charge(cls, invoice_id, agreement_id, amount, idempotency_key):
        response_json = PaypalRequestService.post(
            url=PaypalEndpointService.CREATE_PAYMENT_ENDPOINT,
            data={
                "intent": "sale",
                "payer":
                    {
                        "payment_method": "PAYPAL",
                        "funding_instruments": [
                            {
                                "billing":
                                    {
                                        "billing_agreement_id": agreement_id
                                    }
                            }]
                    },
                "transactions": [
                    {
                        "amount":
                            {
                                "currency": "USD",
                                "total": amount
                            },
                        "description": f'Invoice {invoice_id}',
                        "note_to_payee": f'Invoice {invoice_id}',
                        "invoice_number": invoice_id
                    }],
                "redirect_urls":
                    {
                        "return_url": "https://.com/return",
                        "cancel_url": "https://.com/cancel"
                    }
            },
            idempotency_key=idempotency_key
        )
        status = cls.handle_payment_transaction_detail(response_json)
        return status, response_json

    @classmethod
    def get_payment_detail(cls, sale_id):
        response_json = PaypalRequestService.get(
            url=PaypalEndpointService.GET_SALE_DETAIL_ENDPOINT.format(sale_id=sale_id),
            data={},
        )
        order_transaction_detail = cls.rebuild_payment_transaction_detail(sale_transaction_detail=response_json)
        status = cls.handle_payment_transaction_detail(order_transaction_detail)
        return status, order_transaction_detail

    @classmethod
    def rebuild_payment_transaction_detail(cls, sale_transaction_detail, **kwargs):
        return {
            **kwargs,
            "id": None,
            "links": [],
            "state": "approved",
            "intent": "sale",
            "transactions": [
                {
                    "related_resources": [
                        {
                            "sale": sale_transaction_detail
                        }
                    ]
                }
            ]
        }

    @classmethod
    def handle_payment_transaction_detail(cls, response_json):
        status = TransactionStatus.CHARGE_FAILED
        paypal_payment_state = response_json.get("state")
        if paypal_payment_state == "approved":
            related_transactions = response_json.get("transactions", [])
            if len(related_transactions):
                related_sales = related_transactions[0].get("related_resources")
                if len(related_sales):
                    related_sale = related_sales[0].get("sale", {})
                    sale_state = related_sale.get("state")
                    if sale_state == "completed":
                        status = TransactionStatus.SUCCESS
                    elif sale_state in ("denied", "partially_refunded", "refunded"):
                        status = TransactionStatus.CHARGE_FAILED
                    elif sale_state == "pending":
                        status = TransactionStatus.TRANSACTION_PENDING
        elif paypal_payment_state == "created":
            status = TransactionStatus.TRANSACTION_PENDING
        else:
            status = TransactionStatus.CHARGE_FAILED
        return status

    @classmethod
    def get_transaction_id(cls, transaction_detail):
        return transaction_detail.get("transactions", [{}])[0].get("related_resources", [{}])[0].get("sale", {}).get(
            "id")


def paypal_auto_charge(invoice, paypal_payment_method, idempotency_key):
    status, detail = PaypalSaleService.charge(invoice.payment_gateway_invoice_id, paypal_payment_method.agreement_id,
                                              invoice.total_cost, idempotency_key)
    return status, detail
