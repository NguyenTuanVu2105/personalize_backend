from PIL import Image
from django.http import HttpResponse

from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericAPIView
from abstract_product.models import AbstractProductMockupInfo
from abstract_product.serializers.abstract_product_mockup_infos import AbstractProductMockupInfoSerializer
from abstract_product.services.mockup_info_service import upload_cut_image, get_cut_image_download_url


class CutImageAPIView(AdminGenericAPIView):
    def get(self, request):
        image_path = request.GET.get('image_path')
        url = get_cut_image_download_url(image_path)

        return Response({'url': url})


class CutImageUploadAPIView(AdminGenericAPIView):
    def post(self, request):
        image_file = request.FILES.get('cut_image')
        image = Image.open(image_file)
        mockup_info_id = request.POST.get('mockup_info_id')
        mockup_info = AbstractProductMockupInfo.objects.get(pk=mockup_info_id)

        side_index = int(request.POST.get('side_index'))
        part_index = int(request.POST.get('part_index'))

        new_mockup_info = upload_cut_image(image, image_file.name, mockup_info, side_index, part_index)
        return Response(AbstractProductMockupInfoSerializer(new_mockup_info).data)
