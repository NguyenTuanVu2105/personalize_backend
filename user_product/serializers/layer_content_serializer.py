from rest_framework import serializers

from user_product.models import Artwork, TextPersonalization


class LayerContentSerializer(serializers.RelatedField):
    def to_representation(self, value):
        layer_content = value.layer_content
        if isinstance(layer_content, Artwork):
            from user_product.serializers import ArtworkSerializer
            serializer_data = ArtworkSerializer(instance=layer_content).data

        elif isinstance(layer_content, TextPersonalization):
            from user_product.serializers import MockupTextPersonalizationSerializer
            serializer_data = MockupTextPersonalizationSerializer(instance=layer_content).data

        else:
            serializer_data = None
            # raise Exception('Unexpected type of tagged object')

        return serializer_data

    def to_internal_value(self, data):
        pass
