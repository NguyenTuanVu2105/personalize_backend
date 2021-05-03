from HUB.serializers.generic_relation_serializers import GenericRelationSerializer
from billing.models import Invoice


class GenericRelationInvoiceSerializer(GenericRelationSerializer):
    class Meta(GenericRelationSerializer.Meta):
        model = Invoice
