from django.conf import settings

from HUB.services import HubImageService
from ...constants.image_constants import ARTWORK_THUMBNAIL_SIZE, MOCKUP_THUMBNAIL_SIZE

artwork_image_service = HubImageService(image_dir=settings.ARTWORK_DIRECTORY,
                                        image_extension="png",
                                        thumbnail_size=ARTWORK_THUMBNAIL_SIZE,
                                        save_original_image_as_private=True)

artwork_default_image_service = HubImageService(image_dir=settings.ARTWORK_DEFAULT_DIRECTORY,
                                                image_extension="png",
                                                thumbnail_size=ARTWORK_THUMBNAIL_SIZE,
                                                save_original_image_as_private=True)

mockup_image_service = HubImageService(image_dir=settings.MOCKUP_DIRECTORY,
                                       image_extension="jpeg",
                                       thumbnail_size=MOCKUP_THUMBNAIL_SIZE,
                                       save_original_image_as_private=False)
