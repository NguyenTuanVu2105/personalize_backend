import logging
import urllib

from .gs_abstract_service import GSAbstractService

logger = logging.getLogger(__name__)


class GSFileService(GSAbstractService):
    def upload_private_file(self, *args, **kwargs):
        return self.upload_file(self._private_storage, *args, **kwargs)

    def upload_public_file(self, *args, **kwargs):
        return self.upload_file(self._public_storage, *args, **kwargs)

    def upload_file(self, storage, output_file_path, file):
        storage.save(output_file_path, file)
        return self._get_file_url(storage, output_file_path)

    def delete_public_file(self, file_path):
        return self.delete_file(self._public_storage, file_path)

    def delete_private_file(self, file_path):
        return self.delete_file(self._private_storage, file_path)

    @staticmethod
    def delete_file(storage, file_path):
        unquote_path = urllib.parse.unquote(file_path)
        if storage.exists(unquote_path):
            return storage.delete(unquote_path)
        else:
            logger.info("FILE DOES NOT EXIST!!")
            return None


gs_file_service = GSFileService()
