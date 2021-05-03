from rest_framework.decorators import action
from rest_framework import mixins
from HUB.permissions import get_permissions, method_permission_required
from HUB.services.chunk_cloud_storage_uploader import ChunkCloudStorageUploader
from HUB.viewsets.base import AdminGenericViewSet
from admin_tools.functions.save_image import save_image
from admin_tools.models import AdminImageUploaded
from admin_tools.serializers.admin_image_uploaded import AdminImageUploadedSerializer
from rest_framework.response import Response

class AdminUploadImageViewSet(AdminGenericViewSet, mixins.ListModelMixin):
    queryset = AdminImageUploaded.objects.all()
    serializer_class = AdminImageUploadedSerializer

    @method_permission_required(get_permissions(["admin_image_views"]))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=["POST"], detail=False, url_path="upload", permission_classes=get_permissions("admin_image_upload"))
    def upload(self, request, *args, **kwargs):
        path = request.POST.get('path')
        is_public = request.POST.get('is_public')
        image_obj = save_image(request, path, is_public)
        return Response({"success": True, "image": AdminImageUploadedSerializer(image_obj).data})



