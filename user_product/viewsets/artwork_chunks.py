import logging

from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.services.chunk_cloud_storage_uploader import ChunkCloudStorageUploader
from HUB.throttle import UserThrottle
from HUB.viewsets.base import AuthenticatedGenericViewSet
from user.contants.rate_limit_views import RateLimitView
from user_product.models import Artwork
from user_product.services.artwork import save_artwork
from ..constants import ArtworkStatus
from ..serializers import ArtworkSerializer

logger = logging.getLogger(__name__)


class ArtworkChunkViewSet(AuthenticatedGenericViewSet):
    throttle_classes = [UserThrottle]
    throttle_view = RateLimitView.UPLOAD_ARTWORK_CHUNK
    serializer_class = ArtworkSerializer
    queryset = Artwork.objects.all().select_related("owner").order_by('-create_time')

    @action(methods=["POST"], detail=False, url_path="upload")
    def upload_chunks(self, request, *args, **kwargs):
        resumable_chunk_number = int(request.POST.get('number'))
        resumable_file_id = request.POST.get('file_id')
        chunk_data = request.FILES['file']
        ChunkCloudStorageUploader.save_temp(resumable_file_id, resumable_chunk_number, chunk_data)
        return Response({"status": "ACK"})

    @action(methods=["POST"], detail=False, url_path="merge")
    def merge_chunks(self, request, *args, **kwargs):
        resumable_total_chunks = int(request.POST.get('total'))
        resumable_file_name = request.POST.get('file_name')
        resumable_file_id = request.POST.get('file_id')
        if not ChunkCloudStorageUploader.all_uploaded(resumable_file_id, resumable_total_chunks):
            return Response({"success": False, "message": "Chunks is not uploaded"})
        merged_file = ChunkCloudStorageUploader.merge_chunks(resumable_file_id, resumable_total_chunks)
        logger.info(f'Save merged artwork for user: {request.user.pk}')
        artwork = save_artwork(self.request.user.pk, resumable_file_name, merged_file)
        if request.POST.get('activate'):
            artwork.status = ArtworkStatus.ACTIVE
            artwork.save()
        logger.info(f'Successfully save merged artwork for user: {request.user.pk}, artwork id: {artwork.id}')
        res = ArtworkSerializer(instance=artwork).data
        res["status"] = "FINISHED"
        res["success"] = True
        return Response(res)
