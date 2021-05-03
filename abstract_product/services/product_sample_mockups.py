import logging
import os
import traceback

from .abstract_file_service import sample_mockup_image_service

logger = logging.getLogger(__name__)


def upload_sample_mockups(abstract_product, unchanged_mockups, add_mockups):
    try:
        meta = abstract_product.meta
        template_meta = meta.template_meta
        mockup_urls = []

        for mockup in unchanged_mockups:
            mockup_urls.append({
                "side": "Front",
                "url": mockup
            })

        for mockup in add_mockups:
            prefix = abstract_product.title.lower().replace(" ", "_")
            file_extension = os.path.splitext(mockup.name)[1].strip(".")
            file_url = sample_mockup_image_service.upload_file(file_name_prefix=prefix,
                                                               file_extension=file_extension,
                                                               file_data=mockup)
            mockup_urls.append({
                "side": "Front",
                "url": file_url
            })

        template_meta['mockup_samples'] = mockup_urls
        meta.template_meta = template_meta
        meta.save()
        return True, template_meta

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
