from django.conf import settings

from HUB.services import HubImageService
from abstract_product.constants import CATEGORY_THUMBNAIL_SIZE

category_image_service = HubImageService(image_dir=settings.CATEGORY_IMAGE_DIRECTORY,
                                         image_extension="jpeg",
                                         thumbnail_size=CATEGORY_THUMBNAIL_SIZE,
                                         save_original_image_as_private=False)
#
# product_preview_thumbnail_image_service = HubImageService(image_dir=settings.PRODUCT_PREVIEW_THUMBNAIL_DIRECTORY,
#                                                           image_extension="jpeg",
#                                                           thumbnail_size=PRODUCT_PREVIEW_THUMBNAIL_SIZE,
#                                                           save_original_image_as_private=False)
#
# sample_mockup_image_service = HubImageService(image_dir=settings.PRODUCT_SAMPLE_MOCKUP_DIRECTORY,
#                                               image_extension="jpeg",
#                                               thumbnail_size=MOCKUP_THUMBNAIL_SIZE,
#                                               save_original_image_as_private=False)
#
# design_template_file_service = HubFileService(file_dir=settings.PRODUCT_DESIGN_TEMPLATE_DIRECTORY,
#                                               save_as_private=False)

from HUB.services.cdn_service import CDNService
from HUB.constants import PublicFileType

product_preview_thumbnail_image_service = CDNService(file_type=PublicFileType.PRODUCT_PREVIEW_THUMBNAIL)

sample_mockup_image_service = CDNService(file_type=PublicFileType.PRODUCT_SAMPLE_MOCKUP)

design_template_file_service = CDNService(file_type=PublicFileType.PRODUCT_DESIGN_TEMPLATE)

png_template_file_service = CDNService(file_type=PublicFileType.PNG_TEMPLATE)

sample_mockup_background_service = CDNService(file_type=PublicFileType.PRODUCT_SAMPLE_MOCKUP_BACKGROUND)


def create_product_side_background_service(abstract_product):
    service = CDNService(file_type=PublicFileType.PRODUCT_SIDE_BACKGROUND)
    service.directory += '/{}'.format(abstract_product.title.lower().replace(" ", "_"))
    return service
