import traceback

from django.db import transaction
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet, AdminGenericViewSet
from HUB.viewsets.mixins.list_model_mixins import ListWithUserSettingsModelMixin
from HUB.viewsets.mixins.retrieve_model_mixins import RetrieveWithUserSettingsModelMixin
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from billing.filters import InvoiceFilter
from billing.models import Invoice
from billing.serializers import BriefInvoiceSerializer, InvoiceSerializer
from user_product.models import UserVariant


class AdminInvoiceViewSet(SearchableListModelMixin,
                          RetrieveWithUserSettingsModelMixin,
                          ListWithUserSettingsModelMixin,
                          AdminGenericViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filterset_class = InvoiceFilter

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
