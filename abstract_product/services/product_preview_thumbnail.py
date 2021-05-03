import logging
import os
import traceback

from .abstract_file_service import product_preview_thumbnail_image_service

logger = logging.getLogger(__name__)


def upload_preview_thumbnail(abstract_product, request):
    try:
        prefix = abstract_product.title.lower().replace(" ", "_")
        file_object = request.FILES.get('preview')
        file_extension = os.path.splitext(file_object.name)[1].strip(".")
        file_url = product_preview_thumbnail_image_service.upload_file(file_name_prefix=prefix,
                                                                       file_extension=file_extension,
                                                                       file_data=file_object)
        abstract_product.preview_image_url = file_url
        abstract_product.save()
        return True, file_url

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
