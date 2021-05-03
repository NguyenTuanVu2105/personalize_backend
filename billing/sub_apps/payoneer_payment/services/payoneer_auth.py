import hashlib
import logging
import time

from HUB import settings
from HUB.settings import IDEMPOTENCY_KEY_PREFIX
from billing.sub_apps.payoneer_payment.models.user_payoneer_payment_method import UserPayoneerPaymentMethod
from billing.sub_apps.payoneer_payment.services.payoneer_sdk import PayoneerService

logger = logging.getLogger(__name__)

LOGIN_REDIRECT_URL = f'{settings.PAYONEER_LOGIN_REDIRECT_URL}/?payee={{}}&verify_code={{}}'


def get_login_with_payoneer_link(user, current_shop=None):
    payment_method, created = UserPayoneerPaymentMethod.objects.get_or_create(
        user=user,
        email=None,
        defaults={
            "payee_id": f'{IDEMPOTENCY_KEY_PREFIX}{user.id}_{round(time.time() / 60)}'
        }
    )
    if not created:
        payee_detail = PayoneerService.get_payee_detail(payment_method.payee_id)
        logger.info(payee_detail)
        if payee_detail is None or payee_detail.get("status", "UNKNOWN") == "ACTIVE":
            payment_method.delete()
            payment_method = UserPayoneerPaymentMethod.objects.create(
                user=user,
                email=None,
                payee_id=f'{IDEMPOTENCY_KEY_PREFIX}{user.id}_{round(time.time() / 60)}'
            )

    payee_id = payment_method.payee_id
    verify_code = generate_hash(payee_id, payment_method.id)
    redirect_url = LOGIN_REDIRECT_URL.format(payee_id, verify_code)
    if current_shop is not None:
        redirect_url += "&shop=" + current_shop
    login_link = PayoneerService.create_login_link(payee_id=payee_id, redirect_url=redirect_url)
    return login_link


def generate_hash(payee_id, payment_method_id):
    return hashlib.sha256(f'{settings.OBJECT_ID_PREFIX}_{payee_id}_{payment_method_id}'.encode('utf-8')).hexdigest()


def validate_payoneer_verify_code(payee_id, payment_method, verify_code):
    return verify_code == generate_hash(payee_id, payment_method.id)
