from django.contrib.postgres.aggregates import ArrayAgg
from django.db import transaction
from django.db.models import Manager, QuerySet

from order.constants.fulfill_statuses import OrderPackFulfillStatus, ORDER_PACK_FULFILL_STATUSES_CANCELLABLE


class BaseOrderPackManager(Manager):
    pass


class OrderPackQueryset(QuerySet):
    def unfulfilled(self):
        return self.filter(fulfill_status=OrderPackFulfillStatus.UNFULFILLED)

    def pending(self):
        return self.filter(fulfill_status=OrderPackFulfillStatus.PENDING)

    def requested_fulfillment(self):
        return self.filter(fulfill_status=OrderPackFulfillStatus.REQUESTED_FULFILLMENT)

    def cancellable(self):
        return self.filter(fulfill_status__in=ORDER_PACK_FULFILL_STATUSES_CANCELLABLE)

    def include_item_fulfill_statuses(self):
        return self.annotate(item_fulfill_statuses=ArrayAgg('items__fulfill_status', distinct=True))

    @transaction.atomic
    def bulk_set_canceled(self):
        from billing.models import InvoicePack

        order_packs = self.cancellable()
        order_pack_ids = list(map(lambda pack: pack.id, order_packs))
        InvoicePack.objects.filter(order_pack_id__in=order_pack_ids).bulk_set_canceled()
        self.filter(id__in=order_pack_ids).update(fulfill_status=OrderPackFulfillStatus.CANCELED)
        return order_packs


OrderPackManager = BaseOrderPackManager.from_queryset(OrderPackQueryset)
