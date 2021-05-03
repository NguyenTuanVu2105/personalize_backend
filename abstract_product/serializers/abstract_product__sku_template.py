from rest_framework import serializers

from ..models import SKUTemplate


class SKUTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKUTemplate
        fields = ('sku', 'png_template_url', 'create_time', 'update_time')
