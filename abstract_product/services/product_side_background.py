import logging
import os
import traceback

from .abstract_file_service import create_product_side_background_service
from ..models import AbstractProductMockupInfo

logger = logging.getLogger(__name__)


def upload_product_side_background(abstract_product, side_type, background_file):
    try:
        file_extension = os.path.splitext(background_file.name)[1].strip(".")
        prefix = side_type.lower().replace(' ', '_')

        service = create_product_side_background_service(abstract_product)
        file_url = service.upload_file(file_extension=file_extension,
                                       file_name_prefix=prefix,
                                       file_data=background_file)
        mockups = AbstractProductMockupInfo.objects.filter(abstract_product=abstract_product)
        for mockup in mockups:
            mockup.preview[side_type]['image_path'] = file_url
            mockup.save()

        return True, mockups.first().preview

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
