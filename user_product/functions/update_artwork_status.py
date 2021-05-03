from user_product.models import Artwork


def update_artwork_status(user_product, status):
    for user_product_artwork_fusion in user_product.artwork_set.all():
        artwork_fusion = user_product_artwork_fusion.artwork_fusion
        for artwork_fusion_info in artwork_fusion.artwork_fusion_info_artwork_set.all():
            layer_content = artwork_fusion_info.layer_content
            if isinstance(layer_content, Artwork):
                layer_content.status = status
                layer_content.save()

    return None
