from django.db.models import Manager, QuerySet, Sum, F, DecimalField

from HUB.helpers.sql.functions import Round
from order.constants.fulfill_statuses import OrderItemFulfillStatus


class BaseOrderItemManager(Manager):
    pass


class OrderItemQueryset(QuerySet):
    def aggregate_best_selling_variants(self, limit=10):
        assert isinstance(limit, int)
        return self.values("user_variant").annotate(purchased_quantity=Sum(F("quantity")),
                                                    total_profit=Round(
                                                        Sum(F("quantity") * (F("price_in_usd") - F("mfr_base_cost")),
                                                            output_field=DecimalField()))).order_by(
            "-purchased_quantity", '-total_profit')[:limit]

    def join_abstract_variant(self):
        return self.select_related("user_variant__abstract_variant")

    def accepted_fulfillment(self):
        return self.filter(fulfill_status=OrderItemFulfillStatus.ACCEPTED, quantity__gt=0)

    def can_accepted_fulfillment(self):
        return self.filter(fulfill_status__in=[OrderItemFulfillStatus.HOLDING, OrderItemFulfillStatus.REJECTED],
                           quantity__gt=0)

    def bulk_set_rejected_fulfillment(self):
        return self.accepted_fulfillment().update(fulfill_status=OrderItemFulfillStatus.REJECTED)

    def bulk_set_holding_fulfillment(self):
        return self.accepted_fulfillment().update(fulfill_status=OrderItemFulfillStatus.HOLDING)

    def bulk_set_accept_fulfillment(self):
        return self.can_accepted_fulfillment().update(fulfill_status=OrderItemFulfillStatus.ACCEPTED)


OrderItemManager = BaseOrderItemManager.from_queryset(OrderItemQueryset)
