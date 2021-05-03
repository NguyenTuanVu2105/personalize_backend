from rest_framework import serializers

from ..models import UserFontFamily


class UserFontFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFontFamily
        fields = ('id', 'title', 'font_url', 'description', 'available_characters', 'create_time', 'update_time')
