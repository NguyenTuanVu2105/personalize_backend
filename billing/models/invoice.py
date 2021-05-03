from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models, transaction

from HUB import settings
from HUB.models.random_id_model import RandomIDModel
from billing.constants.invoice_statuses import InvoiceStatus, INVOICE_STATUS_CHOICES
from billing.managers import InvoiceManager
from helper.choice_helpers import find_verbose_type_from_choices
from helper.datetime_helpers import get_current_datetime
from .transaction import Transaction

User = get_user_model()


class Invoice(RandomIDModel):
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="invoices")
    transactions = GenericRelation(Transaction)
    status = models.CharField(max_length=2, choices=INVOICE_STATUS_CHOICES, default=InvoiceStatus.UNPAID, db_index=True)
    paid_time = models.DateTimeField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True)
    idempotency_key = models.CharField(max_length=50, null=True, blank=True)
    charge_count = models.SmallIntegerField(default=0)  # WARNING: ASK THE TEAM LEADER IF YOU WANT TO CHANGE IT -_-
    tsv_metadata_search = SearchVectorField(null=True)

    objects = InvoiceManager()

    class Meta:
        ordering = ['-create_time']
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    def __str__(self):
        return "Invoice  #{}".format(self.id)

    def parse_info(self):
        return {
            "id": self.id
        }

    def get_total_cost(self):
        return self.total_cost

    @property
    def amount(self):
        return self.get_total_cost()

    @property
    def currency(self):
        return "USD"

    @property
    def verbose_status(self):
        return find_verbose_type_from_choices(INVOICE_STATUS_CHOICES, self.status)

    @transaction.atomic
    def set_paid(self):
        self.status = InvoiceStatus.PAID
        self.paid_time = get_current_datetime()
        self.packs.bulk_set_paid()
        self.save()

    @transaction.atomic
    def set_transaction_pending(self):
        self.status = InvoiceStatus.TRANSACTION_PENDING
        self.save()

    @transaction.atomic
    def set_canceled(self):
        self.status = InvoiceStatus.CANCELED
        self.packs.bulk_set_canceled()
        self.save()

    def set_failed(self):
        self.status = InvoiceStatus.FAILED
        self.packs.bulk_set_failed()
        self.save()

    @transaction.atomic
    def set_unpaid(self):
        self.status = InvoiceStatus.UNPAID
        self.packs.bulk_set_unpaid()
        self.save()

    def get_success_transaction(self):
        success_transactions = self.success_transactions or [None]
        return success_transactions[0]

    def get_success_payment_info(self):
        success_transaction = self.get_success_transaction()
        if success_transaction:
            return success_transaction.get_transaction_info()
        else:
            return None, None, None, None

    @property
    def payment_gateway_invoice_id(self):
        return f'{settings.IDEMPOTENCY_KEY_PREFIX}{self.id}'

    @property
    def success_payment_method(self):
        success_transaction = self.get_success_transaction()
        return success_transaction.get_payment_method() if success_transaction else None

    @property
    def is_paid(self):
        return self.status == InvoiceStatus.PAID
