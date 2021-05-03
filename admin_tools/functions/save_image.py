import re

from PIL import Image

from HUB.constants import PublicFileType
from HUB.services import HubImageService, gs_image_service, CDNService
import logging

from admin_tools.models import AdminImageUploaded

logger = logging.getLogger(__name__)

admin_image_public_service = CDNService(file_type=PublicFileType.CUSTOM)
admin_image_private_service = HubImageService(image_dir='', save_original_image_as_private=True)

def save_image(request, path, is_public):
    image = request.FILES.get('image')
    filename, file_extension = str(image.name).split('.')
    prefix_name = re.sub(r'[^0-9a-zA-Z]+', '_', filename)
    if is_public:
        file_url = admin_image_public_service.upload_file(file_name_prefix=prefix_name, file_data=image, file_extension=file_extension, directory=path)
    else:
        real_image = Image.open(image)
        file_url = admin_image_private_service.upload_original_only(file_name_prefix=prefix_name, image=real_image, file_extension=file_extension, dir_path=path)
    original_path = gs_image_service.convert_signed_url_to_file_path(file_url)
    return AdminImageUploaded.objects.create(name=filename, file_url=file_url, path=original_path, path_dir=path, is_public=is_public)