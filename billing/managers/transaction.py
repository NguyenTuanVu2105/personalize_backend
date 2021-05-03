from django.db.models import Manager, QuerySet, Count, Sum, Q, DecimalField
from django.db.models.functions import Coalesce

from HUB.helpers.sql.functions import Round
from billing.constants.transaction_statuses import TransactionStatus
from billing.constants.transaction_types import TransactionType
from billing.functions.get_payment_with_satatistics import get_payment_with_statistics
from billing.sub_apps.combine_payment.constants.payment_method_constants import PAYMENT_GATEWAY_CHOICES


class BaseTransactionManager(Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("payment_method")


class TransactionQueryset(QuerySet):
    def success(self):
        return self.filter(status=TransactionStatus.SUCCESS)

    def pending(self):
        return self.filter(status=TransactionStatus.TRANSACTION_PENDING)

    def filter_charge_type(self):
        return self.filter(type=TransactionType.CHARGE)

    def filter_by_user(self, user_id):
        return self.filter(payment_method__user_setting__user_id=user_id)

    def with_statistics(self, annotate=True, list_payment_gateway=None):
        # If none set all payment gateway
        if not list_payment_gateway:
            list_payment_gateway = [x[0] for x in PAYMENT_GATEWAY_CHOICES]

        # set params for total
        params = {
            "total___count___success": Count('object_id', filter=Q(status=TransactionStatus.SUCCESS)),
            "total___count___charge": Count('object_id', filter=Q(type=TransactionType.CHARGE) & Q(
                status=TransactionStatus.SUCCESS)),
            "total___count___refund": Count('object_id', filter=Q(type=TransactionType.REFUND) & Q(
                status=TransactionStatus.SUCCESS)),
            "total___count___fail": Count('object_id', filter=Q(status__in=[TransactionStatus.TRANSACTION_FAILED, TransactionStatus.TRANSACTION_PENDING])),
            "total___profit___charge": Coalesce(
                Sum('amount', filter=Q(type=TransactionType.CHARGE) & Q(status=TransactionStatus.SUCCESS)), 0),
            "total___profit___refund": Coalesce(
                Sum('amount', filter=Q(type=TransactionType.REFUND) & Q(status=TransactionStatus.SUCCESS)), 0),
            "total___profit___revenue": Round(
                Coalesce(Sum('amount', filter=Q(type=TransactionType.CHARGE) & Q(status=TransactionStatus.SUCCESS)),
                         0) - Coalesce(
                    Sum('amount', filter=Q(type=TransactionType.REFUND) & Q(status=TransactionStatus.SUCCESS)), 0),
                output_field=DecimalField())
        }

        # set params for each payment
        for payment_gateway in list_payment_gateway:
            params.update(get_payment_with_statistics(payment_gateway))

        if annotate:
            return self.annotate(**params)
        else:
            return self.aggregate(**params)


TransactionManager = BaseTransactionManager.from_queryset(TransactionQueryset)
