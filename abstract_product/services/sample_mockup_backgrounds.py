import logging
import os
import traceback

from .abstract_file_service import sample_mockup_background_service

logger = logging.getLogger(__name__)


def upload_sample_mockup_backgrounds(add_mockups, rev_mockups):
    try:
        for mockup in add_mockups:
            file_extension = os.path.splitext(mockup.name)[1].strip(".")
            sample_mockup_background_service.upload_file(file_name_prefix="sample_mockup_background",
                                                         file_extension=file_extension,
                                                         file_data=mockup)
        for mockup in rev_mockups:
            blob_name = mockup.split('/')[-1]
            sample_mockup_background_service.delete_blob_by_name(blob_name=blob_name)

        return True

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
