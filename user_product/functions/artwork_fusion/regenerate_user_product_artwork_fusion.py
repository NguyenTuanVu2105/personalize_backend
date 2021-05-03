import logging

from django.contrib.auth import get_user_model

from . import generate_product_combined_artwork_fusion
from .generate_artwork_fusion import generate_product_artwork_fusion
from ..sample_product import update_sample_product
from ...constants.regenerate_fusion import RegenerateFusionOption
from ...models import UserProductArtworkFusion, ArtworkFusion, ArtworkFusionInfo

User = get_user_model()
logger = logging.getLogger(__name__)


def regenerate_user_product_artwork_fusion(user_product, regenerate_option):
    user_product_artworks = user_product.artwork_set.all()
    combine_fusion = user_product.combine_fusion
    if not combine_fusion:
        for user_product_artwork_fusion in user_product_artworks:
            generate_product_artwork_fusion(user_product_artwork_fusion)
    else:
        if regenerate_option == RegenerateFusionOption.TO_COMBINE_FUSION:
            user_product_artworks.update(send_to_fulfill=False)
            fulfill_user_product_artwork_fusion = update_fulfillment_artwork(user_product, user_product_artworks)
        else:
            fulfill_user_product_artwork_fusion = user_product_artworks.send_to_fulfill_filter().first()

        separated_side_user_product_artwork_fusions = user_product_artworks.send_to_fulfill_exclude()
        generate_product_combined_artwork_fusion(user_product, separated_side_user_product_artwork_fusions,
                                                 fulfill_user_product_artwork_fusion)

    if hasattr(user_product, "created_sample_product"):
        update_sample_product(user_product.created_sample_product)


def update_fulfillment_artwork(user_product, user_product_artworks):
    side = user_product.abstract_product.sides.filter(type="Front").first()
    fulfill_artwork_fusion = ArtworkFusion.objects.create(name=str(user_product.id) + str("_combine"),
                                                          owner_id=user_product.user.id,
                                                          background_color=None)

    artwork_fusion_infos_to_create = []
    for user_product_artwork_fusion in user_product_artworks:
        artwork_fusion = user_product_artwork_fusion.artwork_fusion
        artwork_fusion_info = artwork_fusion.artwork_fusion_info_artwork_set.first()
        if artwork_fusion_info:
            artwork_fusion_infos_to_create.append(ArtworkFusionInfo(artwork=artwork_fusion_info.artwork,
                                                                    frame=fulfill_artwork_fusion,
                                                                    layer=artwork_fusion_info.layer,
                                                                    rotation=artwork_fusion_info.rotation,
                                                                    position=artwork_fusion_info.position,
                                                                    scale=artwork_fusion_info.scale,
                                                                    dnd_scale=artwork_fusion_info.dnd_scale))

    fulfill_user_product_artwork_fusion = UserProductArtworkFusion.objects.create(user_product=user_product,
                                                                                  product_side=side,
                                                                                  send_to_fulfill=True,
                                                                                  artwork_fusion=fulfill_artwork_fusion)
    ArtworkFusionInfo.objects.bulk_create(artwork_fusion_infos_to_create)

    return fulfill_user_product_artwork_fusion
