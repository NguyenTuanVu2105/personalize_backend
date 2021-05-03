import logging

from django.db import transaction

from billing.sub_apps.braintree_payment.services import braintree_deactivate_payment_method
from billing.sub_apps.combine_payment.constants import PaymentGateway
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod
from billing.sub_apps.payoneer_payment.services.payoneer_sdk import PayoneerService
from billing.sub_apps.paypal_payment.services import PaypalBillingAgreementService
from billing.sub_apps.paypal_vault_payment.services.paypal_vault_payment_token_service import \
    PaypalVaultPaymentTokenService
from billing.sub_apps.stripe_payment.functions import stripe_deactivate_payment_method
from notification.enums.instant_prompt_types import InstantPromptType
from notification.services.instant_prompt import remove_instant_prompt

logger = logging.getLogger(__name__)


@transaction.atomic
def create_general_payment_method(payment_gateway_method):
    GeneralPaymentMethod.objects.create(content_object=payment_gateway_method)
    user = payment_gateway_method.user
    if not user.is_valid_payment:
        remove_instant_prompt(user.id, [InstantPromptType.ADD_PAYMENT_METHOD])
        user.is_valid_payment = True
        user.save()

    fix_duplicate_ordinal_number_payment_method(payment_gateway_method.user_id)


@transaction.atomic
def reactivate_general_payment_method(payment_gateway_method):
    affected_row_count = payment_gateway_method.general_payment_methods.update(is_active=True, ordinal_number=0)
    if affected_row_count < 1:
        create_general_payment_method(payment_gateway_method)
    fix_duplicate_ordinal_number_payment_method(payment_gateway_method.user_id)


def fix_duplicate_ordinal_number_payment_method(user_id):
    payment_methods = GeneralPaymentMethod.objects.active().by_user(user_id)
    payment_method_ids = [payment_method.pk for payment_method in payment_methods]
    reorder_payment_methods(payment_method_ids, payment_methods)


@transaction.atomic
def reorder_payment_methods(new_payment_method_order, payment_methods):
    id_with_index_dict = {v: (k + 1) for k, v in enumerate(new_payment_method_order)}
    for pm in payment_methods:
        pm.ordinal_number = id_with_index_dict[pm.id]
        pm.save()


@transaction.atomic
def deactivate_payment_method(general_payment_method):
    try:
        deactivate_related_payment_gateway_method(general_payment_method.content_object)
    except Exception as e:
        logger.exception(e)
    general_payment_method.deactivate()
    fix_duplicate_ordinal_number_payment_method(general_payment_method.content_object.user_id)


def deactivate_related_payment_gateway_method(payment_gateway_method):
    payment_gateway = payment_gateway_method.gateway_name
    is_success = False
    if payment_gateway == PaymentGateway.STRIPE:
        is_success = stripe_deactivate_payment_method(payment_gateway_method)
    elif payment_gateway == PaymentGateway.BRAINTREE:
        is_success = braintree_deactivate_payment_method(payment_gateway_method)
    elif payment_gateway == PaymentGateway.PAYONEER:
        is_success = PayoneerService.delete_payee(payment_gateway_method.payee_id)
    elif payment_gateway == PaymentGateway.PAYPAL_PRO:
        is_success = PaypalBillingAgreementService.deactivate(payment_gateway_method.agreement_id)
    elif payment_gateway == PaymentGateway.PAYPAL_VAULT:
        is_success = PaypalVaultPaymentTokenService.deactivate(payment_gateway_method.payment_token)
    return is_success
