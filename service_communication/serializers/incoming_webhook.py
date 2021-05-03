from generic_relations.relations import GenericRelatedField
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from order.models.order import Order
from order.serializers import GenericRelationOrderSerializer
from service_communication.models import IncomingWebhook


class IncomingWebhookSerializer(ModelSerializer):
    relate_object = GenericRelatedField({
        Order: GenericRelationOrderSerializer(),
    })
    type = CharField(source="verbose_type")
    status = CharField(source="verbose_status")

    class Meta:
        model = IncomingWebhook
        fields = (
            "id", "relate_object", "type", "body_data", "status", "meta", "process_description", "process_count", "create_time", "update_time")
