import logging
from datetime import datetime, timedelta

from django.conf import settings

from user_product.constants import ArtworkStatus
from user_product.functions.storage import artwork_image_service
from user_product.models import Artwork

logger = logging.getLogger(__name__)


def delete_unused_artworks(self_delete):
    logger.info("SCHEDULED_DELETE_UNUSED_ARTWORK RUNNING")
    unused_artworks = Artwork.objects.filter(
        status__in=[ArtworkStatus.UPLOADED, ArtworkStatus.AD_CLONED, ArtworkStatus.SP_CLONED],
        create_time__lte=datetime.now() - timedelta(
            seconds=settings.TIME_TO_DELETE_UNUSED_ARTWORK))
    for artwork in unused_artworks:
        # artwork.delete_artwork(self_delete)
        artwork_name = artwork.name
        if artwork.status == ArtworkStatus.UPLOADED:
            artwork_image_service.delete_original_image(artwork.original_image_path)
            artwork_image_service.delete_thumnail_image(artwork.thumbnail_image_path)
        if self_delete:
            artwork.delete()
        logger.info("DELETED ARTWORK ".format(artwork_name))
    return None
