import logging
import time

from django.db import transaction

from .paypal_vault_payment_token_service import PaypalVaultPaymentTokenService
from billing.sub_apps.paypal_vault_payment.models import PaypalVaultPaymentMethod

logger = logging.getLogger(__name__)


class PaypalVaultPaymentMethodService:
    SYNC_PAYMENT_METHOD_TIME_OUT = 10
    SYNC_PAYMENT_METHOD_DELAY = 2

    @classmethod
    def check_payment_methods(cls, customer_id):
        start_time = time.time()
        while (time.time() - start_time) < cls.SYNC_PAYMENT_METHOD_TIME_OUT:
            is_success = cls.sync_payment_methods(customer_id)
            if is_success:
                return True
            time.sleep(cls.SYNC_PAYMENT_METHOD_DELAY)
        return False

    @classmethod
    def sync_payment_methods(cls, customer_id):
        response_json = PaypalVaultPaymentTokenService.list_payment_tokens_by_customer_id(customer_id)
        logger.info(response_json)
        payment_tokens = set()
        for payment_token_obj in response_json:
            if not payment_token_obj.get("status") == "CREATED":
                continue
            token_id = payment_token_obj.get("id")
            payment_tokens.add(token_id)
        added_paypal_vault_payment_methods = set(
            PaypalVaultPaymentMethod.objects.filter(user_id=customer_id).values_list("payment_token", flat=True))
        new_paypal_vault_payment_methods = payment_tokens - added_paypal_vault_payment_methods
        if len(new_paypal_vault_payment_methods) == 0:
            return False
        with transaction.atomic():
            for token_id in new_paypal_vault_payment_methods:
                payment_token_obj = PaypalVaultPaymentTokenService.get_payment_token_detail(token_id)
                card = payment_token_obj.get("source", {}).get("card", {})
                type = card.get("brand")
                last4 = card.get("last_digits")
                exp_year, exp_month = card.get("expiry", "-").split("-")

                PaypalVaultPaymentMethod.objects.create(user_id=customer_id, payment_token=token_id,
                                                        card_name="", type=type, last4=last4,
                                                        exp_month=exp_month, exp_year=exp_year)
            return True
