import logging
import os
import traceback

from .abstract_file_service import png_template_file_service
from ..models import SKUTemplate

logger = logging.getLogger(__name__)


def upload_png_design_template(abstract_product, png_template_file):
    try:
        abstract_sku = abstract_product.sku
        prefix = abstract_sku.lower()
        file_extension = os.path.splitext(png_template_file.name)[1].strip(".")
        file_url = png_template_file_service.upload_file(file_name_prefix=prefix,
                                                         file_extension=file_extension,
                                                         file_data=png_template_file)
        sku_template = SKUTemplate.objects.update_or_create(sku=abstract_sku, defaults={'png_template_url': file_url})
        return True, file_url

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
