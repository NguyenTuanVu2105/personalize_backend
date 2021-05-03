import os

from django.utils import timezone
from google.cloud import storage

from HUB import settings
from HUB.constants import FILE_TYPE_TO_DIRECTORY
from HUB.helpers.randox_hex import random_hex

ASSETS_CDN_URL = settings.ASSETS_CDN_URL


class CDNService:
    CDN_STORAGE = storage.Client(project=None, credentials=settings.GS_PUBLIC_CREDENTIALS)
    CDN_BUCKET = CDN_STORAGE.get_bucket(settings.GS_PUBLIC_BUCKET_NAME)

    def __init__(self, file_type):
        self.directory = FILE_TYPE_TO_DIRECTORY[file_type]

    @staticmethod
    def get_temp_path(dir, name):
        return os.path.join(dir, name)

    def get_blob(self, file_name, directory=None):
        _directory = directory if directory else self.directory
        file_path = self.get_temp_path(_directory, file_name)
        blob = self.CDN_BUCKET.blob(file_path)
        return blob

    def upload_file(self, file_name_prefix, file_data, file_extension, directory=None):
        millis_timestamp = int(timezone.now().timestamp() * 1000)
        file_name = "{name_prefix}_{timestamp}_{random_hex}.{file_extension}".format(name_prefix=file_name_prefix,
                                                                                     timestamp=millis_timestamp,
                                                                                     random_hex=random_hex(10),
                                                                                     file_extension=file_extension)
        blob = self.get_blob(file_name, directory)
        content_type = self.get_content_type(file_extension)
        if content_type:
            blob.upload_from_file(file_obj=file_data, predefined_acl="publicRead", content_type=content_type)
        else:
            blob.upload_from_file(file_obj=file_data, predefined_acl="publicRead")

        return self.get_public_url_from_blob(blob)

    def get_public_url_from_file_name(self, file_name):
        blob = self.get_blob(file_name)
        return self.get_public_url_from_blob(blob)

    @staticmethod
    def get_public_url_from_blob(blob):
        return "{}/{}".format(ASSETS_CDN_URL, blob.name)

    @staticmethod
    def get_content_type(file_extension):
        lower_file_extension = file_extension.lower()
        if lower_file_extension == 'png':
            content_type = 'image/png'
        elif lower_file_extension == 'jpg' or lower_file_extension == 'jpeg':
            content_type = 'image/jpeg'
        else:
            content_type = None

        return content_type

    def list_public_object_urls(self, folder_path):
        blobs_list = self.CDN_STORAGE.list_blobs(bucket_or_name=settings.GS_PUBLIC_BUCKET_NAME, prefix=folder_path)
        blob_url_list = []
        for blob in blobs_list:
            blob_url_list.append(self.get_public_url_from_blob(blob=blob))

        return blob_url_list

    def delete_blob_by_name(self, blob_name):
        blob = self.get_blob(blob_name)
        return self.delete_blob(blob)

    @staticmethod
    def delete_blob(blob):
        return blob.delete()
