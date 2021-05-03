from rest_framework import serializers

from user.serializers.user import BriefUserSerializer
from ..models import UserFontFamily


class AdminFontFamilySerializer(serializers.ModelSerializer):
    owner = BriefUserSerializer()

    class Meta:
        model = UserFontFamily
        fields = ('id', 'title', 'font_url', 'is_active', 'owner', 'description', 'available_characters',
                  'used_frequency', 'create_time', 'update_time')
