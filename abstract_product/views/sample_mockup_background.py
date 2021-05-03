import logging
import traceback

from django.conf import settings
from rest_framework.response import Response

from HUB.viewsets.base import BaseGenericAPIView
from abstract_product.services import sample_mockup_background_service

logger = logging.getLogger(__name__)


class SampleMockupBackgroundAPIView(BaseGenericAPIView):
    @staticmethod
    def get(request):
        try:
            sample_mockup_bg_path = settings.SAMPLE_MOCKUP_BACKGROUND_DIRECTORY
            result = sample_mockup_background_service.list_public_object_urls(
                folder_path=sample_mockup_bg_path) if sample_mockup_bg_path else []
            return Response({"success": True, "data": result})

        except Exception as e:
            logger.info(str(e))
            traceback.print_tb(e.__traceback__)
            return Response({"success": False, "message": str(e)})
