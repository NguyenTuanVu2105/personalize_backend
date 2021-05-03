from datetime import datetime, timedelta

from billing.sub_apps.payoneer_payment.models import UserPayoneerPaymentMethod


def remove_invalid_payee_ids():
    clear_time = datetime.now() - timedelta(days=30)
    UserPayoneerPaymentMethod.objects. \
        filter(general_payment_methods__isnull=True, update_time__lt=clear_time). \
        delete()
