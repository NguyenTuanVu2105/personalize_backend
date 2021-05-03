import os

from PIL import Image
from django.utils import timezone

from HUB.helpers.randox_hex import random_hex
from .gs_image_service import gs_image_service


class HubImageService:
    def __init__(self, image_dir, image_extension="png", thumbnail_size=256,
                 save_original_image_as_private=True):
        base_image_dir = "{image_dir}/{{image_type}}".format(
            image_dir=image_dir)
        self.base_original_image_dir = base_image_dir.format(image_type="originals")
        self.base_thumbnail_image_dir = base_image_dir.format(image_type="thumbnails")
        self.save_original_image_as_private = save_original_image_as_private
        self.image_extension = image_extension
        self.thumbnail_size = thumbnail_size

    def upload(self, file_name_prefix, image, raw_data_file=None, file_extension=None):
        millis_timestamp = int(timezone.now().timestamp() * 1000)
        image_name = "{name_prefix}_{timestamp}_{random_hex}.{file_extension}".format(name_prefix=file_name_prefix,
                                                                                      timestamp=millis_timestamp,
                                                                                      random_hex=random_hex(10),
                                                                                      file_extension=file_extension if file_extension else self.image_extension)

        original_image_path = os.path.join(self.base_original_image_dir, image_name)
        thumbnail_image_path = os.path.join(self.base_thumbnail_image_dir, image_name)
        if raw_data_file is None:
            original_image_url = self._upload_original(original_image_path, image, self.save_original_image_as_private)
        else:
            original_image_url = self._upload_raw_original(original_image_path, raw_data_file,
                                                           self.save_original_image_as_private)
        thumbnail_image_url = self._upload_thumbnail(thumbnail_image_path, image)
        return original_image_url, thumbnail_image_url

    def upload_original_only(self, file_name_prefix, image, raw_data_file=None, file_extension=None, dir_path=None):
        millis_timestamp = int(timezone.now().timestamp() * 1000)
        image_name = "{name_prefix}_{timestamp}_{random_hex}.{file_extension}".format(name_prefix=file_name_prefix,
                                                                                      timestamp=millis_timestamp,
                                                                                      random_hex=random_hex(10),
                                                                                      file_extension=file_extension if file_extension else self.image_extension)
        image_dir = dir_path if dir_path else self.base_original_image_dir
        original_image_path = os.path.join(image_dir, image_name)
        if raw_data_file is None:
            original_image_url = self._upload_original(original_image_path, image, self.save_original_image_as_private)
        else:
            original_image_url = self._upload_raw_original(original_image_path, raw_data_file,
                                                           self.save_original_image_as_private)
        return original_image_url

    def _upload_original(self, path, image, private=True):
        if not private:
            return gs_image_service.upload_public_image(path, image)
        return gs_image_service.upload_private_image(path, image)

    def _upload_raw_original(self, path, raw_data, private=True):
        if not private:
            return gs_image_service.upload_public_raw_data(path, raw_data)
        return gs_image_service.upload_private_raw_data(path, raw_data)

    def _upload_thumbnail(self, path, image):
        thumbnail = self._generate_thumbnail(image)
        return gs_image_service.upload_public_image(path, thumbnail)

    def _generate_thumbnail(self, image):
        width, height = image.size
        if width > self.thumbnail_size and height > self.thumbnail_size:
            if width > height:
                width = int(width * self.thumbnail_size / height)
                height = self.thumbnail_size
            else:
                height = int(height * self.thumbnail_size / width)
                width = self.thumbnail_size
            return image.resize((width, height), Image.ANTIALIAS)
        else:
            return image

    def delete_thumnail_image(self, path):
        return gs_image_service.delete_public_image(path)

    def delete_original_image(self, path):
        return gs_image_service.delete_private_image(path)
