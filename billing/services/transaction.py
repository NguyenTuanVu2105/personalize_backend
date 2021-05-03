import logging

from billing.constants.transaction_types import TransactionType
from billing.forms import TransactionCreationForm

logging.basicConfig()
logger = logging.getLogger(__name__)


def save_new_transaction(transaction_type, payment_method, data):
    data = {**data, "type": transaction_type, "payment_method": payment_method and payment_method.pk}
    form = TransactionCreationForm(data=data)
    if form.is_valid():
        transaction_obj = form.save()
        logger.info("Saved new {} transaction".format(transaction_obj.verbose_type))
        return transaction_obj.pk
    else:
        logger.warning("Transaction validation error: {}".format(form.errors))


def save_new_refund_transaction(*args, **kwargs):
    return save_new_transaction(TransactionType.REFUND, *args, **kwargs)
