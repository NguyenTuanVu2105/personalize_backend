import logging

from rest_framework import serializers

from abstract_product.models import AbstractProductMockupInfo

logger = logging.getLogger(__name__)


class AbstractProductMockupInfoSerializer(serializers.ModelSerializer):
    preview = serializers.JSONField()

    def to_representation(self, obj):
        abstract_product = obj.abstract_product
        active_mockup_version = abstract_product.active_mockup_version
        representation = super().to_representation(obj)
        mockup_infos = representation['meta']['mockup_infos']
        if type(mockup_infos).__name__ == 'dict' and active_mockup_version in mockup_infos:
            representation['meta']['mockup_infos'] = mockup_infos.pop(active_mockup_version)
        return representation

    class Meta:
        model = AbstractProductMockupInfo
        fields = ('id', 'name', 'preview', 'preview_meta', 'meta')
