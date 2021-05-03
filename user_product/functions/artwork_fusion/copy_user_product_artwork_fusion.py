import logging

from django.db.models.functions import Now

from abstract_product.models import AbstractProductSide
from user_product.models import UserProductArtworkFusion, ArtworkFusion, ArtworkFusionInfo

logger = logging.getLogger(__name__)


def copy_user_product_artwork_fusion(user_product_artwork_fusion):
    user_product = user_product_artwork_fusion.user_product
    artwork_fusion = user_product_artwork_fusion.artwork_fusion

    user_product_artwork_fusion_to_create = []
    artwork_fusion_info_to_create = []

    for additional_fusion_side in user_product.additional_fusion_sides:
        side = AbstractProductSide.objects.filter(type=additional_fusion_side).first()
        additional_user_product_artwork_fusion = UserProductArtworkFusion.objects.filter(product_side=side,
                                                                                         user_product=user_product,
                                                                                         send_to_fulfill=True).first()
        if not additional_user_product_artwork_fusion:
            additional_artwork_fusion = ArtworkFusion.objects.create(owner_id=artwork_fusion.owner_id,
                                                                     name=artwork_fusion.name,
                                                                     original_image_path=artwork_fusion.original_image_path,
                                                                     image_url=artwork_fusion.image_url,
                                                                     background_color=artwork_fusion.background_color,
                                                                     last_fusion_update_time=Now())
            for artwork_fusion_info in artwork_fusion.artwork_fusion_info_artwork_set.all():
                new_artwork_fusion_info = ArtworkFusionInfo(layer_type=artwork_fusion_info.layer_type,
                                                            layer_content_type=artwork_fusion_info.layer_content_type,
                                                            layer_content_id=artwork_fusion_info.layer_content_id,
                                                            frame=additional_artwork_fusion,
                                                            layer=artwork_fusion_info.layer,
                                                            rotation=artwork_fusion_info.rotation,
                                                            position=artwork_fusion_info.position,
                                                            scale=artwork_fusion_info.scale,
                                                            dnd_scale=artwork_fusion_info.dnd_scale,
                                                            is_hidden=artwork_fusion_info.is_hidden)
                artwork_fusion_info_to_create.append(new_artwork_fusion_info)

            new_user_product_artwork_fusion = UserProductArtworkFusion(user_product=user_product,
                                                                       product_side=side,
                                                                       artwork_fusion=additional_artwork_fusion,
                                                                       send_to_fulfill=True)
            user_product_artwork_fusion_to_create.append(new_user_product_artwork_fusion)

        else:
            additional_artwork_fusion = additional_user_product_artwork_fusion.artwork_fusion
            additional_artwork_fusion.original_image_path = artwork_fusion.original_image_path
            additional_artwork_fusion.image_url = artwork_fusion.image_url
            additional_artwork_fusion.last_fusion_update_time = Now()
            additional_artwork_fusion.save()

    UserProductArtworkFusion.objects.bulk_create(user_product_artwork_fusion_to_create)
    ArtworkFusionInfo.objects.bulk_create(artwork_fusion_info_to_create)

    return None
