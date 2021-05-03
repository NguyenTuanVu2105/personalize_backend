from datetime import timedelta

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum, F, DecimalField, Count, Q, ExpressionWrapper, Manager, DateTimeField
from django.db.models.functions import Coalesce

from HUB.helpers.sql.functions import Round
from HUB.managers.querysets import NullsAreSmallestQuerySet
from billing.constants.invoice_pack_statuses import InvoicePackStatus
from helper.datetime_helpers import get_current_datetime
from order.constants.financial_statuses import OrderFinancialStatus
from order.constants.fulfill_statuses import OrderFulfillStatus, OrderPackFulfillStatus


class BaseOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("customer_info", "shipping_rate")


class OrderQueryset(NullsAreSmallestQuerySet):
    def are_item_editable(self):
        return self.filter(fulfill_status=OrderFulfillStatus.UNFULFILLED)

    def last_created_earlier_x_min_ago(self, x):
        return self.filter(create_time__lte=get_current_datetime() - timedelta(minutes=x))

    def edit_order_items_delay_was_expired(self):
        current_time = get_current_datetime()
        return self.filter(request_order_processing_manually=False).annotate(
            order_items_are_editable_until=ExpressionWrapper(F("edit_order_items_delay") + F("seller_edit_time"),
                                                             output_field=DateTimeField())).filter(
            order_items_are_editable_until__lte=current_time)

    def include_pack_fulfill_statuses(self):
        return self.annotate(pack_fulfill_statuses=ArrayAgg('packs__fulfill_status', distinct=True))

    def include_pack_financial_statuses(self):
        return self.annotate(pack_financial_statuses=ArrayAgg('packs__invoice_pack__status', filter=~Q(
            packs__fulfill_status__in=[OrderPackFulfillStatus.CANCELED, OrderPackFulfillStatus.REJECTED]) & ~Q(
            packs__invoice_pack__status__in=[InvoicePackStatus.CANCELED]), distinct=True))

    def filter_by_user_id(self, user_id):
        return self.filter(shop__owner_id=user_id)

    def with_statistics(self, annotate=True):
        params = {
            "count__ids": Count("items", distinct=True, output_field=DecimalField()),
            "est_profit___sale_price": Round(
                Sum(F("total_price_in_usd") / F("total_items"),
                    output_field=DecimalField())),
            "est_profit___production_cost": Round(
                Sum(F('production_cost') / F("total_items"),
                    output_field=DecimalField())),
            "est_profit___shipping_cost": Round(
                Coalesce(Sum(F('shipping_cost') / F("total_items"),
                             output_field=DecimalField()), 0)),
            "est_profit___amount": F(
                "est_profit___sale_price") - F("est_profit___production_cost") - F(
                "est_profit___shipping_cost"),
            "count___total": Count(
                "id", distinct=True),
            "count___fulfill_status___unfulfilled": Count(
                "id", filter=Q(
                    fulfill_status__in=(OrderFulfillStatus.UNFULFILLED, OrderFulfillStatus.PENDING)), distinct=True),
            "count___fulfill_status___fulfilled": Count(
                "id", filter=Q(
                    fulfill_status__in=(OrderFulfillStatus.PARTIALLY_FULFILLED,
                                        OrderFulfillStatus.FULFILLED)), distinct=True),
            "count___fulfill_status___requested": Count(
                "id", filter=Q(
                    fulfill_status__in=(OrderFulfillStatus.REQUESTED_FULFILLMENT,)), distinct=True),
            "count___fulfill_status___in_production": Count(
                "id", filter=Q(
                    fulfill_status__in=(OrderFulfillStatus.PARTIALLY_IN_PRODUCTION,
                                        OrderFulfillStatus.IN_PRODUCTION)), distinct=True),
            "count___fulfill_status___canceled": Count(
                "id", filter=Q(
                    fulfill_status__in=(OrderFulfillStatus.CANCELED,
                                        OrderFulfillStatus.CANCELED_SHIPPING)), distinct=True),
            "count___fulfill_status___rejected": Count(
                "id", filter=Q(
                    fulfill_status__in=(OrderFulfillStatus.REJECTED,)), distinct=True),

            "count___financial_status___paid": Count(
                "id", filter=Q(
                    financial_status__in=(OrderFinancialStatus.PARTIALLY_PAID, OrderFinancialStatus.PAID)),
                distinct=True),
            "count___financial_status___unpaid": Count(
                "id", filter=Q(
                    financial_status=OrderFinancialStatus.PENDING), distinct=True),
            "count___financial_status___cancelled": Count(
                "id", filter=Q(
                    financial_status=OrderFinancialStatus.CANCELED), distinct=True),
            "count___financial_status___failed": Count(
                "id", filter=Q(
                    financial_status=OrderFinancialStatus.FAILED), distinct=True),
        }
        if annotate:
            return self.annotate(**params)
        else:
            return self.aggregate(**params)

    def has_shop_filter(self):
        return self.exclude(shop__isnull=True)


OrderManager = BaseOrderManager.from_queryset(OrderQueryset)
