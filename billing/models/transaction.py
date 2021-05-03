from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from HUB.models.random_id_model import RandomIDModel
from billing.constants.transaction_statuses import TRANSACTION_STATUS_CHOICES
from billing.constants.transaction_types import TRANSACTION_TYPE_CHOICES
from billing.managers import TransactionManager
from billing.sub_apps.combine_payment.constants.payment_method_constants import PAYMENT_GATEWAY_CHOICES
from billing.sub_apps.combine_payment.models import GeneralPaymentMethod
from helper.choice_helpers import find_verbose_type_from_choices


class Transaction(RandomIDModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    amount = models.DecimalField(max_digits=11, decimal_places=2, db_index=True)
    type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=2, db_index=True)
    payment_gateway = models.CharField(choices=PAYMENT_GATEWAY_CHOICES, max_length=2, db_index=True)
    payment_gateway_transaction_id = models.CharField(max_length=50, null=True, blank=True)
    payment_method = models.ForeignKey(to=GeneralPaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(choices=TRANSACTION_STATUS_CHOICES, max_length=2, db_index=True)
    detail = JSONField()
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)
    idempotency_key = models.CharField(max_length=50, null=True, blank=True)
    tsv_metadata_search = SearchVectorField(null=True)

    objects = TransactionManager()

    class Meta:
        ordering = ["-create_time", "-id"]
        indexes = [GinIndex(fields=["tsv_metadata_search"])]

    @property
    def payment_gateway_transaction_detail(self):
        return self.detail

    @property
    def user(self):
        return self.payment_method.user_setting.user

    def get_transaction_info(self):
        return self.payment_gateway, self.payment_method, self.payment_gateway_transaction_id, self.payment_gateway_transaction_detail

    def get_payment_method(self):
        if self.payment_method:
            return self.payment_method.payment_gateway_method_data

    def get_owner(self):
        return self.payment_method.user_setting.user

    def get_content_object_info(self):
        if self.content_object:
            return self.content_object.parse_info()

    @property
    def verbose_type(self):
        return find_verbose_type_from_choices(TRANSACTION_TYPE_CHOICES, self.type)

    @property
    def is_responded_by_payment_gateway(self):
        return bool(self.payment_gateway_transaction_id)

    @property
    def order_ids(self):
        from order.models.order import Order
        from billing.models.refund import Refund
        from billing.models.invoice import Invoice
        content_obj = self.content_object
        data = []
        if isinstance(content_obj, Invoice):
            data = list(content_obj.packs.values_list('order_pack__order_id', flat=True).distinct().order_by())
        elif isinstance(content_obj, Refund):
            obj = content_obj.content_object
            if isinstance(obj, Order):
                data = [obj.id]
        return data
