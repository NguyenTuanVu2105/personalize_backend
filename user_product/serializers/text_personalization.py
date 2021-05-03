from rest_framework import serializers

from user_product.models import TextPersonalization
from user_product.serializers import UserFontFamilySerializer


class MockupTextPersonalizationSerializer(serializers.ModelSerializer):
    font_family_url = serializers.StringRelatedField(source="font_family.font_url")

    class Meta:
        model = TextPersonalization
        fields = ('id', 'raw_svg', 'text', 'font_family_url')


class DetailTextPersonalizationSerializer(serializers.ModelSerializer):
    font_family = UserFontFamilySerializer()

    class Meta:
        model = TextPersonalization
        fields = (
            'id', 'placeholder_label', 'text', 'text_color', 'font_family', 'text_size', 'text_spacing',
            'outline_color', 'outline_thickness', 'shadow_color', 'shadow_distance', 'shadow_angle', 'arc',
            'is_allow_customize', 'create_time', 'update_time', 'raw_svg')
