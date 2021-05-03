from abstract_product.models import AbstractProduct, AbstractProductSide
from user_product.models import ArtworkDefault

import logging

logger = logging.getLogger(__name__)


def sync_artwork_default():
    try:
        default_artworks = ArtworkDefault.objects.all()
        default_artwork_update_list = []
        for default_artwork in default_artworks:
            try:
                sku = default_artwork.product_sku
                product_side = default_artwork.product_side
                if sku and product_side:
                    abstract_product = AbstractProduct.objects.filter(sku=sku, is_active=True).first()
                    side = AbstractProductSide.objects.filter(abstract_product_id=abstract_product.id,
                                                              type=product_side.type).first()
                    default_artwork.product_side = side
                    default_artwork_update_list.append(default_artwork)
            except Exception as e:
                logger.error(e)
        ArtworkDefault.objects.bulk_update(default_artwork_update_list, ["product_side"])
    except Exception as e:
        logger.error(e)
