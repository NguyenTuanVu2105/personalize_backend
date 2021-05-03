from rest_framework import serializers

from user.serializers.user import BriefUserSerializer
from user_product.models import UploadedMockup


class UploadedMockupSerializer(serializers.ModelSerializer):
    owner = BriefUserSerializer()

    class Meta:
        model = UploadedMockup
        fields = ('id', 'owner', 'file_url', 'create_time')