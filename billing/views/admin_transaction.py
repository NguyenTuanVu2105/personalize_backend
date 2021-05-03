from HUB.permissions import get_permissions, method_permission_required
from HUB.viewsets.base import AdminGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from billing.filters import TransactionFilter
from billing.models import Transaction
from billing.serializers.transaction import AdminTransactionSerializer


class AdminTransactionViewSet(SearchableListModelMixin,
                              AdminGenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = AdminTransactionSerializer
    filterset_class = TransactionFilter

    def get_queryset(self):
        return self.queryset

    @method_permission_required(get_permissions(['admin_transaction_view', ]))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)