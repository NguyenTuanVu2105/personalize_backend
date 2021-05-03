from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB import settings
from HUB.models.random_id_model import RandomIDModel
from billing.constants.refund_statuses import REFUND_STATUSES, RefundStatus
from billing.constants.refund_types import REFUND_TYPES, RefundType, REFUND_TYPE_DICT
from billing.managers import RefundManager
from billing.models import Invoice
from helper.choice_helpers import find_verbose_type_from_choices


def default_refund_info():
    return {
        "refunded_items": ""
    }


class Refund(RandomIDModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE, related_name="refunds")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    refund_type = models.CharField(max_length=2, choices=REFUND_TYPES, default=RefundType.CANCEL_SHIPPING)
    description = models.CharField(max_length=255, null=True, blank=True)
    info = JSONField(default=default_refund_info)
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=11, blank=True)
    currency = models.CharField(max_length=30, blank=True, default="USD")
    status = models.CharField(max_length=2, choices=REFUND_STATUSES, default=RefundStatus.IN_REVIEW)
    approve_time = models.DateTimeField(auto_now_add=False, null=True)
    tsv_metadata_search = SearchVectorField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    objects = RefundManager()

    class Meta:
        ordering = ['-create_time']
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    def __str__(self):
        return "Refund #{}".format(self.id)

    def set_settled(self):
        self.set_status(RefundStatus.SETTLED)

    def set_failed(self):
        self.set_status(RefundStatus.FAILED)

    def set_status(self, status):
        self.status = status
        self.save()

    def parse_info(self):
        return {
            "id": self.id,
            "invoice": self.invoice.parse_info(),
        }

    @property
    def verbose_status(self):
        return find_verbose_type_from_choices(REFUND_STATUSES, self.status)

    @property
    def verbose_refund_type(self):
        return REFUND_TYPE_DICT.get(self.refund_type)

    @property
    def is_retryable(self):
        return self.status == RefundStatus.FAILED

    @property
    def is_approvable(self):
        return self.status == RefundStatus.IN_REVIEW

    @property
    def content_type_label(self):
        return self.content_type.app_label