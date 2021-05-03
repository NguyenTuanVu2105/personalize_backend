from django.http import HttpResponse
from rest_framework.response import Response

from HUB.services.chunk_cloud_storage_uploader import ChunkCloudStorageUploader
from HUB.viewsets.base import AdminGenericAPIView
from abstract_product.models import AbstractProductMockupInfo
from abstract_product.serializers.admin_abstract_product import AbstractProductMockupInfoSerializer
from abstract_product.services.mockup_info_service import upload_model_file, get_model_file_download_url


class ModelFileAPIView(AdminGenericAPIView):
    def get(self, request):
        model_path = request.GET.get('model_path')
        url = get_model_file_download_url(model_path)

        return Response({'url': url})


class ModelFileUploadChunkAPIView(AdminGenericAPIView):
    def post(self, request):
        resumable_chunk_number = int(request.POST.get('number'))
        resumable_file_id = request.POST.get('file_id')
        chunk_data = request.FILES['file']
        ChunkCloudStorageUploader.save_temp(resumable_file_id, resumable_chunk_number, chunk_data)
        return Response({"status": "ACK"})


class ModelFileMergeChunkAPIView(AdminGenericAPIView):
    def post(self, request):
        resumable_total_chunks = int(request.POST.get('total'))
        resumable_file_name = request.POST.get('file_name')
        resumable_file_id = request.POST.get('file_id')
        mockup_info_id = request.POST.get('mockup_info_id')
        side_index = int(request.POST.get('side_index'))
        part_index = int(request.POST.get('part_index'))
        mockup_info = AbstractProductMockupInfo.objects.get(pk=mockup_info_id)
        if not ChunkCloudStorageUploader.all_uploaded(resumable_file_id, resumable_total_chunks):
            return Response({"success": False, "message": "Chunks is not uploaded"})
        merged_file = ChunkCloudStorageUploader.merge_chunks(resumable_file_id, resumable_total_chunks)

        upload_model_file(merged_file, resumable_file_name, mockup_info, side_index, part_index)
        return Response(AbstractProductMockupInfoSerializer(mockup_info).data)
