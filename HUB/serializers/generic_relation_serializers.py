from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from HUB.models.random_id_model import RandomIDModel


class GenericRelationSerializer(ModelSerializer):
    type = CharField(source="model_name")

    class Meta:
        model = RandomIDModel
        fields = ('id', "type")
