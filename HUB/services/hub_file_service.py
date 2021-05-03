import os

from django.utils import timezone

from .gs_file_service import gs_file_service


class HubFileService:
    def __init__(self, file_dir, save_as_private=True):
        self.base_file_dir = file_dir
        self.save_as_private = save_as_private

    def upload(self, file, file_name, file_extension):
        millis_timestamp = int(timezone.now().timestamp() * 1000)
        updated_file_name = "{name_prefix}_{timestamp}.{file_extension}".format(name_prefix=file_name,
                                                                                timestamp=millis_timestamp,
                                                                                file_extension=file_extension)
        original_file_path = os.path.join(self.base_file_dir, updated_file_name)
        original_file_url = self._upload_original(original_file_path, file, self.save_as_private)
        return original_file_url

    @staticmethod
    def _upload_original(path, file, private=True):
        if not private:
            return gs_file_service.upload_public_file(path, file)
        return gs_file_service.upload_private_file(path, file)

    @staticmethod
    def delete_original_file(path):
        return gs_file_service.delete_private_file(path)
