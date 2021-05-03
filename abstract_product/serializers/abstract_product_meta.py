from rest_framework import serializers

from ..models import AbstractProductMeta


class AbstractProductMetaSerializer(serializers.ModelSerializer):
    pricing_meta = serializers.JSONField()

    class Meta:
        model = AbstractProductMeta
        fields = (
            'id', 'base_cost', 'description', 'pricing_meta', 'abstract_product', 'shipping_meta', 'template_meta','design_note')


class AbstractProductMetaForSampleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractProductMeta
        fields = ('id', 'base_cost', 'abstract_product', 'shipping_meta','design_note')
