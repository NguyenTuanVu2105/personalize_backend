from rest_framework import serializers

from ..models import AbstractProductSide


class AbstractProductSideSerializer(serializers.ModelSerializer):
    constraints = serializers.JSONField()
    fusion_size = serializers.JSONField()

    class Meta:
        model = AbstractProductSide
        fields = ('id', 'type', 'constraints', 'fusion_size', 'enable_background_color')


class BriefSideSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractProductSide
        fields = ('id', 'type')