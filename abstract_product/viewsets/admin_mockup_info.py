from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericViewSet
from abstract_product.models import AbstractProductMockupInfo
from abstract_product.serializers.admin_abstract_product import AbstractProductMockupInfoSerializer
from abstract_product.services import get_cut_image_download_url, get_model_file_download_url


class AdminMockupInfoViewSet(AdminGenericViewSet):
    queryset = AbstractProductMockupInfo.objects.all()
    serializer_class = AbstractProductMockupInfoSerializer

    @action(methods=['GET'], detail=True, url_path='get-backup')
    def get_mockup_info_backup(self, request, *args, **kwargs):
        mockup_info = self.get_object()
        mockup_meta = mockup_info.meta
        side_mockup_infos = mockup_meta.get('mockup_infos')
        consistency_name = mockup_meta.get('consistency_name')
        response_dict = {'cut_image': [], 'model': []}

        for side_mockup_info in side_mockup_infos:
            if side_mockup_info.get('type') == 'no-handle':
                continue
            for part in side_mockup_info.get('parts'):
                cut_image = get_cut_image_download_url(f'{consistency_name}/{part.get("image_path")}')
                if "model" in part:
                    model = get_model_file_download_url(f'{part.get("model")}')
                    response_dict['model'].append({
                        'name': part.get("model"),
                        'url': model
                    })
                response_dict['cut_image'].append({
                    'name': part.get("image_path"),
                    'url': cut_image
                })
                
        return Response(response_dict)
