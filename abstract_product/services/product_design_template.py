import logging
import os
import traceback

from .abstract_file_service import design_template_file_service

logger = logging.getLogger(__name__)


def upload_design_template(abstract_product, design_template_file):
    try:
        meta = abstract_product.meta
        template_meta = meta.template_meta

        prefix = abstract_product.title.lower().replace(" ", "_")
        file_extension = os.path.splitext(design_template_file.name)[1].strip(".")
        file_url = design_template_file_service.upload_file(file_name_prefix=prefix,
                                                            file_extension=file_extension,
                                                            file_data=design_template_file)

        template_meta['template_url'] = file_url
        meta.template_meta = template_meta
        meta.save()

        return True, template_meta

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
