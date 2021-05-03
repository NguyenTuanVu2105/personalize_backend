from user_product.models import ArtworkFusion, ArtworkFusionInfo, UserProductArtworkFusion


def sync_artwork_fusion_info(user_product, side_fusion_infos):
    artwork_fusion_info_to_create = []
    user_product_artwork_fusion_to_create = []
    delete_old_separated_side_artwork_relations(user_product)

    for side_fusion_info in side_fusion_infos:
        side_type = side_fusion_info['side']
        side = user_product.abstract_product.sides.filter(type=side_type).first()
        artwork_fusion_name = "{}_{}".format(user_product.id, side_type)
        artwork_fusion = ArtworkFusion.objects.create(owner=user_product.user, name=artwork_fusion_name,
                                                      background_color=user_product.background_color)
        for artwork_info in side_fusion_info['artwork_infos']:
            artwork_fusion_info_to_create.append(ArtworkFusionInfo(artwork_id=artwork_info['id'],
                                                                   frame=artwork_fusion,
                                                                   layer=artwork_info['layer'],
                                                                   scale=artwork_info['scale'],
                                                                   position=artwork_info['position'],
                                                                   rotation=artwork_info['rotation'],
                                                                   dnd_scale=artwork_info['dnd_scale']))

        user_product_artwork_fusion_to_create.append(UserProductArtworkFusion(user_product=user_product,
                                                                              artwork_fusion=artwork_fusion,
                                                                              product_side=side,
                                                                              send_to_fulfill=False))

    ArtworkFusionInfo.objects.bulk_create(artwork_fusion_info_to_create)
    UserProductArtworkFusion.objects.bulk_create(user_product_artwork_fusion_to_create)


def delete_old_separated_side_artwork_relations(user_product):
    separated_side_user_product_artwork_fusions = user_product.artwork_set.send_to_fulfill_exclude()
    for separated_side_user_product_artwork_fusion in separated_side_user_product_artwork_fusions:
        separated_side_artwork_fusion = separated_side_user_product_artwork_fusion.artwork_fusion
        separated_side_artwork_fusion.artwork_fusion_info_artwork_set.all().delete()
        separated_side_artwork_fusion.delete()
    separated_side_user_product_artwork_fusions.delete()
