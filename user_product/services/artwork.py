import hashlib
import logging
import os
import re
from datetime import datetime

from PIL import Image

from HUB.services import gs_image_service
from user_product.constants import ArtworkStatus
from user_product.functions.storage import artwork_image_service
from user_product.models import Artwork

logger = logging.getLogger(__name__)

Image.MAX_IMAGE_PIXELS = 250000000


def save_artwork(owner_id, file_name, merged_file):
    filename, file_extension = os.path.splitext(file_name)
    file_extension = file_extension[1:]
    prefix_name = re.sub(r'[^0-9a-zA-Z]+', '_', filename)
    readable_hash = hashlib.sha256(merged_file.read()).hexdigest()
    artwork_image = Image.open(merged_file)
    artwork_image_width, artwork_image_height = artwork_image.size
    # start_millis_timestamp = int(timezone.now().timestamp() * 1000)
    artwork_url, artwork_thumbnail_url = artwork_image_service.upload(file_name_prefix=prefix_name,
                                                                      image=artwork_image,
                                                                      raw_data_file=merged_file,
                                                                      file_extension=file_extension)

    storage_artwork_path = gs_image_service.convert_signed_url_to_file_path(artwork_url)
    storage_thumbnail_path = gs_image_service.convert_signed_url_to_file_path(artwork_thumbnail_url)
    merged_file.close()
    # end_millis_timestamp = int(timezone.now().timestamp() * 1000)
    # logger.info("----------- total time for saving: {}".format((end_millis_timestamp - start_millis_timestamp) / 1000))
    artwork = Artwork.objects.create(owner_id=owner_id, name=filename,
                                     original_image_path=storage_artwork_path,
                                     thumbnail_image_path=storage_thumbnail_path,
                                     file_url=artwork_thumbnail_url, sha256=readable_hash,
                                     width=artwork_image_width, height=artwork_image_height,
                                     status=ArtworkStatus.UPLOADED,
                                     last_used_time=datetime.utcnow())

    return artwork


def update_artwork(artwork, prefix_name, name, merged_file):
    prefix_name = re.sub(r'[^0-9a-zA-Z]+', '_', prefix_name)
    readable_hash = hashlib.sha256(merged_file.read()).hexdigest()
    artwork_image = Image.open(merged_file)
    artwork_image_width, artwork_image_height = artwork_image.size
    artwork_url, artwork_thumbnail_url = artwork_image_service.upload(file_name_prefix=prefix_name,
                                                                      image=artwork_image,
                                                                      raw_data_file=merged_file)
    storage_artwork_path = gs_image_service.convert_signed_url_to_file_path(artwork_url)
    storage_thumbnail_path = gs_image_service.convert_signed_url_to_file_path(artwork_thumbnail_url)
    merged_file.close()

    artwork.original_image_path = storage_artwork_path
    artwork.thumbnail_image_path = storage_thumbnail_path
    artwork.file_url = artwork_thumbnail_url
    artwork.sha256 = readable_hash
    artwork.width = artwork_image_width
    artwork.height = artwork_image_height
    artwork.name = name
    artwork.save()
    return artwork
