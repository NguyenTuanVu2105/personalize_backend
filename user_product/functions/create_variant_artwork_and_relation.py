import base64
import logging
import re

from django.contrib.auth import get_user_model
from django.core.files.storage import get_storage_class

from abstract_product.models import AbstractProductSide
from user_product.constants import ArtworkStatus
from user_product.models import ArtworkFusion, Artwork, ArtworkFusionInfo
from user_product.models.user_variant_artwork_fusion import UserVariantArtworkFusion
from user_product.services.artwork import save_artwork

logger = logging.getLogger(__name__)
User = get_user_model()
media_storage = get_storage_class()()


def create_variant_artwork_and_relation(user_variant, artworks, image_url, seller_id):
    for artwork_by_side in artworks:
        side_id = artwork_by_side['side']["id"]
        side = AbstractProductSide.objects.get(id=side_id)
        for index, artwork in enumerate(artwork_by_side['artworksList']):
            if 'id' in artwork:
                artwork_object = Artwork.objects.get(id=artwork['id'])
                artwork_object.status = ArtworkStatus.ACTIVE
                artwork_object.save()
            else:
                artwork_name = artwork['name']
                artwork_data = re.sub('^data:image/.+;base64,', '',
                                      artwork['data'])

                byte_data = base64.b64decode(artwork_data)
                artwork_object = save_artwork(seller_id, str(side), artwork_name, byte_data)

            artwork_fusion = ArtworkFusion.objects.create(name=artwork_object.name,
                                                          original_image_path=artwork_object.original_image_path,
                                                          image_url=image_url,
                                                          owner_id=seller_id)
            UserVariantArtworkFusion.objects.create(user_variant=user_variant, variant_side=side,
                                                    artwork_fusion=artwork_fusion)

            ArtworkFusionInfo.objects.create(artwork_id=artwork_object.id, frame=artwork_fusion, layer=index + 1,
                                             rotation=artwork['rotation'], position=artwork['position'],
                                             scale=artwork['scale'])
