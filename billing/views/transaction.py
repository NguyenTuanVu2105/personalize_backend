from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from billing.filters import TransactionFilter
from billing.models import Transaction
from billing.serializers import TransactionSerializer


class TransactionViewSet(SearchableListModelMixin,
                         AuthenticatedGenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter

    def get_queryset(self):
        return self.queryset.filter(payment_method__user_setting__user__id=self.request.user.pk)
