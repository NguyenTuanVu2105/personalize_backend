from django.db.models import Count, Sum, Q, DecimalField
from django.db.models.functions import Coalesce

from HUB.helpers.sql.functions import Round
from billing.constants.transaction_statuses import TransactionStatus
from billing.constants.transaction_types import TransactionType
from billing.sub_apps.combine_payment.constants.payment_method_constants import PAYMENT_GATEWAY_CHOICES
from helper.choice_helpers import find_verbose_type_from_choices


def get_payment_with_statistics(payment_gateway):
    verbose_payment_gateway = find_verbose_type_from_choices(PAYMENT_GATEWAY_CHOICES, payment_gateway)
    return {
        "{}___count___success".format(verbose_payment_gateway): Count('object_id',
                                                                      filter=Q(payment_gateway=payment_gateway) & Q(
                                                                          status=TransactionStatus.SUCCESS)),
        "{}___count___charge".format(verbose_payment_gateway): Count('object_id',
                                                                     filter=Q(type=TransactionType.CHARGE) & Q(
                                                                         payment_gateway=payment_gateway) & Q(
                                                                         status=TransactionStatus.SUCCESS)),
        "{}___count___refund".format(verbose_payment_gateway): Count('object_id',
                                                                     filter=Q(type=TransactionType.REFUND) & Q(
                                                                         payment_gateway=payment_gateway) & Q(
                                                                         status=TransactionStatus.SUCCESS)),
        "{}___count___fail".format(verbose_payment_gateway): Count('object_id', filter=Q(
            status__in=[TransactionStatus.TRANSACTION_FAILED, TransactionStatus.TRANSACTION_PENDING]) & Q(
            payment_gateway=payment_gateway)),
        "{}___profit___charge".format(verbose_payment_gateway): Coalesce(
            Sum('amount', filter=Q(type=TransactionType.CHARGE) & Q(payment_gateway=payment_gateway) & Q(
                status=TransactionStatus.SUCCESS)), 0),
        "{}___profit___refund".format(verbose_payment_gateway): Coalesce(
            Sum('amount', filter=Q(type=TransactionType.REFUND) & Q(payment_gateway=payment_gateway) & Q(
                status=TransactionStatus.SUCCESS)), 0),
        "{}___profit___revenue".format(verbose_payment_gateway): Round(Coalesce(
            Sum('amount', filter=Q(type=TransactionType.CHARGE) & Q(payment_gateway=payment_gateway) & Q(
                status=TransactionStatus.SUCCESS)),
            0) - Coalesce(
            Sum('amount', filter=Q(type=TransactionType.REFUND) & Q(payment_gateway=payment_gateway) & Q(
                status=TransactionStatus.SUCCESS)), 0),
                                                                       output_field=DecimalField())
    }
