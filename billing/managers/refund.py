from django.db.models import Manager

from billing.constants.refund_statuses import RefundStatus


class RefundManager(Manager):
    def pending(self):
        return self.get_queryset().filter(status=RefundStatus.PENDING)
