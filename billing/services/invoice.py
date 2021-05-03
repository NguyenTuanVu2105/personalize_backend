import logging
from threading import Lock

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator

from billing.models import Invoice, InvoicePack, InvoiceItem

User = get_user_model()
logging.basicConfig()
logger = logging.getLogger(__name__)

lock = Lock()


class InvoiceService:
    INVOICE_TOTAL_COST_THRESHOLD = 100000000
    INVOICE_TOTAL_PACK_THRESHOLD = 5

    @staticmethod
    def create_new_fulfillment_invoice_pack(new_pack):
        invoice_pack = InvoicePack.objects.create(order_pack=new_pack,
                                                  production_cost=new_pack.production_cost,
                                                  shipping_cost=new_pack.shipping_cost,
                                                  discount=new_pack.discount,
                                                  currency=new_pack.currency)
        for order_item in new_pack.items.all():
            InvoiceItem.objects.create(invoice_pack=invoice_pack,
                                       order_item=order_item,
                                       quantity=order_item.quantity,
                                       price=order_item.production_cost)

    @classmethod
    def create_invoice(cls):
        user_objs = User.objects.all()
        for user_obj in user_objs:
            cls.create_invoice_by_user(user_obj=user_obj)

    @classmethod
    def create_invoice_by_user(cls, user_obj):
        while True:
            invoice_packs = InvoicePack.objects.filter(invoice=None,
                                                       order_pack__order__shop__owner_id=user_obj.pk).order_by(
                "update_time")[:cls.INVOICE_TOTAL_PACK_THRESHOLD]
            invoice_pack_count = len(invoice_packs)
            if not len(invoice_packs):
                break
            logger.info("Merge {} invoice pack(s) owned by user_id {}".format(invoice_pack_count, user_obj.pk))
            mergeable_invoice_pack_ids = []
            total_invoice_price = 0
            for invoice_pack in invoice_packs:
                mergeable_invoice_pack_ids.append(invoice_pack.id)
                total_invoice_price += invoice_pack.total_cost
                if total_invoice_price > cls.INVOICE_TOTAL_COST_THRESHOLD:
                    break
            cls.merge_invoice_pack_to_invoice(user_obj, mergeable_invoice_pack_ids)

    @staticmethod
    @method_decorator(transaction.atomic)
    def merge_invoice_pack_to_invoice(user_obj, invoice_pack_ids):
        if len(invoice_pack_ids) > 0:
            invoice = Invoice.objects.create_with_customer(customer=user_obj)
            InvoicePack.objects.filter(id__in=invoice_pack_ids).merge_to_new_invoice(invoice_obj=invoice)
            transaction.on_commit(lambda: invoice.save())  # trigger post_save signals
