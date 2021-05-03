from urllib.parse import urlparse

from django.core.files.storage import DefaultStorage
from google.cloud.storage.blob import _API_ACCESS_ENDPOINT


class GSAbstractService:
    def __init__(self):
        self._init_private_storage()
        self._init_public_storage()

    def _init_private_storage(self):
        self._private_storage = DefaultStorage()

    def _init_public_storage(self):
        self._public_storage = DefaultStorage()
        self._public_storage.default_acl = 'publicRead'

    def _get_file_instance(self, storage, file_path, mode="wb"):
        return storage.open(file_path, mode)

    def convert_private_file_path_to_signed_url(self, *args, **kwargs):
        return self._get_file_url(self._private_storage, *args, **kwargs)

    def convert_signed_url_to_file_path(self, signed_url):
        url_path = urlparse(signed_url).path
        file_path = url_path.split("/", 1)[-1]
        return file_path

    def _get_file_url(self, storage, file_path):
        """
        Example URI:
            https://storage.googleapis.com/fulfillment-hub/transparent-images/originals/mug-white-front.png
        """
        if not file_path:
            return ""
        validated_file_path = storage.url(file_path).replace(_API_ACCESS_ENDPOINT, "").split("/", 2)[-1]
        bucket_name = storage.bucket.name
        full_url = _API_ACCESS_ENDPOINT.replace("://", "://{}.".format(bucket_name)) + "/" + validated_file_path
        return full_url

    def get_public_url(self, file_path):
        return self._get_file_url(self._public_storage, file_path)

    def list_public_object_urls(self, folder_path):
        blobs_list = self._public_storage.listdir(folder_path)[1]
        blob_url_list = []
        for blob_name in blobs_list:
            if blob_name:
                file_path = f'{folder_path}/{blob_name}'
                blob_url_list.append(self.get_public_url(file_path=file_path))

        return blob_url_list
