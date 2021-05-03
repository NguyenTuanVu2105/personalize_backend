from generic_relations.relations import GenericRelatedField
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from order.models.order import Order
from order.serializers import GenericRelationOrderSerializer
from service_communication.models import RejectedRequest
from user.serializers.user import BriefUserSerializer


class RequestRejectedSerializer(ModelSerializer):
    relate_object = GenericRelatedField({
        Order: GenericRelationOrderSerializer(),
    })
    request_type = CharField(source="verbose_request_type")
    status = CharField(source="verbose_status")
    last_update_user = BriefUserSerializer()

    class Meta:
        model = RejectedRequest
        fields = (
            "id", "relate_object", "request_type", "detail", "status", "note", "last_update_user", "create_time")
