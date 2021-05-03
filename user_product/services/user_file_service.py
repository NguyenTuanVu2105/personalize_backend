from HUB.constants import PublicFileType
from HUB.services.cdn_service import CDNService
from HUB.services.gs_file_service import gs_file_service

# mockup_service = CDNService(file_type=PublicFileType.USER_PRODUCT_MOCKUP)
font_service = gs_file_service
# font_service = CDNService(file_type=PublicFileType.USER_FONT)
