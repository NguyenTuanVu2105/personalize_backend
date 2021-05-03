from __future__ import absolute_import, unicode_literals

import logging
import os
import traceback
from datetime import datetime, timedelta

from django.conf import settings

from HUB.services import gs_image_service
from user_product.constants import TIME_TO_DELETE_UNUSED_MOCKUPS
from user_product.models import UploadedMockup, UserVariantSideMockup

logger = logging.getLogger(__name__)


def delete_unused_mockups():
    try:
        timedelta_to_scan = timedelta(seconds=TIME_TO_DELETE_UNUSED_MOCKUPS)
        recent_mockups = UploadedMockup.objects.filter(create_time__lte=datetime.now() - timedelta_to_scan)
        if os.environ.get("USE_S3") == "TRUE":
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        else:
            bucket_name = settings.GS_BUCKET_NAME
        for uploaded_mockup in recent_mockups:
            file_url = uploaded_mockup.file_url
            existed = UserVariantSideMockup.objects.filter(mockup_url=file_url)
            if len(existed) == 0:
                file_path = file_url.split(f"/{bucket_name}/")[-1]
                logger.info(f"Delete unused file: {file_path}")
                gs_image_service.delete_public_image(image_path=file_path)
            uploaded_mockup.delete()

    except Exception as e:
        logger.exception(str(e))
        traceback.print_tb(e.__traceback__)
        raise Exception
