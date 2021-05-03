import logging
import os
import urllib
from io import BytesIO

from .gs_abstract_service import GSAbstractService

logger = logging.getLogger(__name__)


class GSImageService(GSAbstractService):
    def upload_private_image(self, *args, **kwargs):
        return self.upload_image(self._private_storage, *args, **kwargs)

    def upload_public_image(self, *args, **kwargs):
        return self.upload_image(self._public_storage, *args, **kwargs)

    def upload_private_raw_data(self, *args, **kwargs):
        return self.upload_raw_data(self._private_storage, *args, **kwargs)

    def upload_public_raw_data(self, *args, **kwargs):
        return self.upload_raw_data(self._public_storage, *args, **kwargs)

    def upload_raw_data(self, storage, output_image_path, raw_data_file):
        storage.save(output_image_path, raw_data_file)
        return self._get_file_url(storage, output_image_path)

    def upload_image(self, storage, output_image_path, image):
        file_extension = self.standard_file_extension(os.path.splitext(output_image_path)[1].strip("."))
        with BytesIO() as buffer:
            image.save(buffer, file_extension)
            storage.save(output_image_path, buffer)
        return self._get_file_url(storage, output_image_path)

    def standard_file_extension(self, ext):
        if ext.lower() == "jpg":
            return "JPEG"
        else:
            return ext.upper()

    def delete_public_image(self, image_path):
        return self.delete_image(self._public_storage, image_path)

    def delete_private_image(self, image_path):
        return self.delete_image(self._private_storage, image_path)

    @staticmethod
    def delete_image(storage, image_path):
        unquote_path = urllib.parse.unquote(image_path)
        if storage.exists(unquote_path):
            return storage.delete(unquote_path)
        else:
            logger.info("FILE DOES NOT EXIST!!")
            return None


gs_image_service = GSImageService()
