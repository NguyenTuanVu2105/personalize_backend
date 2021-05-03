from rest_framework.serializers import ModelSerializer

from admin_tools.models import AdminImageUploaded


class AdminImageUploadedSerializer(ModelSerializer):
    class Meta:
        model = AdminImageUploaded
        fields = ("id", "name", "file_url", "is_public", "path", "path_dir", "create_time", "update_time")