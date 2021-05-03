from django.db.models import Sum, DecimalField, Count, ExpressionWrapper, Manager

from order.constants.cancel_shipping_request_statuses import CancelShippingRequestStatus


class CancelShippingRequestManager(Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            total_shipping_cost=ExpressionWrapper(Sum('order_packs__shipping_cost') / Count("order_packs__items", distinct=True),
                                                  output_field=DecimalField()))

    def pending(self):
        return self.get_queryset().filter(status=CancelShippingRequestStatus.PENDING)
