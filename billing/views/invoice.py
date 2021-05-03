import traceback

from django.db import transaction
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.list_model_mixins import ListWithUserSettingsModelMixin
from HUB.viewsets.mixins.retrieve_model_mixins import RetrieveWithUserSettingsModelMixin
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from billing.filters import InvoiceFilter
from billing.models import Invoice
from billing.serializers import BriefInvoiceSerializer, InvoiceSerializer
from user_product.models import UserVariant


class InvoiceViewSet(SearchableListModelMixin,
                     RetrieveWithUserSettingsModelMixin,
                     ListWithUserSettingsModelMixin,
                     AuthenticatedGenericViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filterset_class = InvoiceFilter
    ordering_fields = ['total_cost']

    def get_queryset(self):
        return self.queryset.filter(customer_id=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        self.serializer_class = BriefInvoiceSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Invoice.objects.select_related("customer").prefetch_related("packs__order_pack",
                                                                                    "packs__items__order_item",
                                                                                    "packs__order_pack__order__shop",
                                                                                    Prefetch(
                                                                                        "packs__items__order_item__user_variant",
                                                                                        UserVariant.objects.prefetch_related_objects()))
        return super().retrieve(request, *args, *kwargs)

    @action(methods=["POST"], detail=False, url_path="retry")
    @method_decorator(transaction.atomic)
    def recharge_failed_invoices(self, request):
        success = False
        user = request.user
        user_settings = user.settings
        request_data = request.data
        order_ids = request_data.get("order_ids")
        order_ids = [] if not isinstance(order_ids, list) else order_ids
        invoice_ids = request_data.get("invoice_ids") or []
        invoice_ids = [] if not isinstance(invoice_ids, list) else invoice_ids
        if request.user.settings.is_invoices_charge_unlockable:
            try:
                user_settings.unlock_invoices_charge()
                invoice_queryset = user.invoices.failed()
                if order_ids:
                    invoice_queryset = invoice_queryset.filter(packs__order_pack__order_id__in=order_ids)
                if invoice_ids:
                    invoice_queryset = invoice_queryset.filter(id__in=invoice_ids)

                for invoice_obj in invoice_queryset:
                    invoice_obj.set_unpaid()
            except Exception as e:
                traceback.print_tb(e.__traceback__)
            else:
                success = True
        return Response({"success": success})
