import logging
import traceback

from django.conf import settings
from rest_framework.response import Response

from HUB.permissions import method_permission_required, get_permissions
from HUB.viewsets.base import AdminGenericAPIView
from abstract_product.services import sample_mockup_background_service
from abstract_product.services.sample_mockup_backgrounds import upload_sample_mockup_backgrounds

logger = logging.getLogger(__name__)


class AdminSampleMockupBackgroundAPIView(AdminGenericAPIView):
    @method_permission_required(get_permissions(['admin_sample_product_view', ]))
    def get(self, request):
        try:
            sample_mockup_bg_path = settings.SAMPLE_MOCKUP_BACKGROUND_DIRECTORY
            result = sample_mockup_background_service.list_public_object_urls(
                folder_path=sample_mockup_bg_path) if sample_mockup_bg_path else []
            return Response({"success": True, "data": result})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})

    @method_permission_required(get_permissions(['admin_sample_product_add', 'admin_sample_product_delete', ]))
    def put(self, request):
        try:
            success = upload_sample_mockup_backgrounds(request.FILES.getlist('add_mockups'),
                                                       request.data.getlist('rev_mockups'))
            sample_mockup_bg_path = settings.SAMPLE_MOCKUP_BACKGROUND_DIRECTORY
            result = sample_mockup_background_service.list_public_object_urls(
                folder_path=sample_mockup_bg_path) if sample_mockup_bg_path else []
            return Response({"success": success, "data": result})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})
