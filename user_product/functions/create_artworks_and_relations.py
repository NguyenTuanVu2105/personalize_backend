import logging

from django.contrib.auth import get_user_model
from django.core.files.storage import get_storage_class
from django.db.models.functions import Now

from abstract_product.models import AbstractProductSide
from user_product.constants import ArtworkStatus
from user_product.constants.artwork_fusion_info_metas import LayerType
from user_product.forms import TextPersonalizationForm
from user_product.models import UserProductArtworkFusion, ArtworkFusion, Artwork, ArtworkFusionInfo

logger = logging.getLogger(__name__)
User = get_user_model()
media_storage = get_storage_class()()


def create_artworks_and_relations(user_product, side_layers, seller_id):
    user_product_id = user_product.id
    artwork_id_list = []
    user_product_artwork_fusions_to_create = []
    artwork_fusions_to_create = []
    artwork_fusion_infos_to_create = []

    sides = AbstractProductSide.objects.only("id", "enable_background_color", "fulfill_require_artwork") \
        .filter(abstract_product_id=user_product.abstract_product_id)
    layer_by_side_dict = dict((side_layer['side']['id'], side_layer) for side_layer in side_layers)

    sides_has_content = []

    if user_product.combine_fusion:
        combine_fusion_handler(user_product_id, seller_id, sides, layer_by_side_dict, artwork_id_list,
                               artwork_fusion_infos_to_create, user_product_artwork_fusions_to_create)

    no_combine_fusion_handler(user_product_id, seller_id, sides, layer_by_side_dict, artwork_id_list,
                              artwork_fusion_infos_to_create, user_product_artwork_fusions_to_create,
                              artwork_fusions_to_create, sides_has_content, not user_product.combine_fusion)

    artwork_object_list = Artwork.objects.filter(id__in=artwork_id_list).only('status')
    for artwork in artwork_object_list:
        if artwork.status not in [ArtworkStatus.ACTIVE, ArtworkStatus.INACTIVE]:
            artwork.status = ArtworkStatus.ACTIVE
        artwork.last_used_time = Now()
        artwork.is_legal_accepted = True
        artwork.total_created_product = artwork.total_created_product + 1

    Artwork.objects.bulk_update(artwork_object_list,
                                ['status', 'last_used_time', 'total_created_product', 'is_legal_accepted'])
    UserProductArtworkFusion.objects.bulk_create(user_product_artwork_fusions_to_create)
    ArtworkFusionInfo.objects.bulk_create(artwork_fusion_infos_to_create)

    # Logged, 4-5 queries, no matter how many ArtworkFusion there are


def artwork_fusion_info_handler(content_by_side, artwork_id_list, artwork_fusion, artwork_fusion_infos_to_create):
    if content_by_side:
        for index, layer in enumerate(content_by_side['layers']):
            layer_index = layer['layerIndex'] if 'layerIndex' in layer else index + 1
            layer_content_obj = None
            if layer['type'] == LayerType.ARTWORK:
                artwork_id = layer['id']
                artwork_id_list.append(artwork_id)
                artwork = Artwork.objects.get(pk=artwork_id)
                layer_content_obj = artwork

            elif layer['type'] == LayerType.PERSONAL_TEXT:
                layer_content = layer['content']
                text_personalization_form = TextPersonalizationForm(
                    data={**layer_content, "font_family": layer_content['font_family_id']})
                text_personalization_form.validate()
                text_personalization = text_personalization_form.save()
                layer_content_obj = text_personalization

            if layer_content_obj:
                artwork_fusion_infos_to_create.append(ArtworkFusionInfo(layer_content=layer_content_obj,
                                                                        frame=artwork_fusion,
                                                                        layer_type=layer['type'],
                                                                        layer=layer_index,
                                                                        rotation=layer['rotation'],
                                                                        position=layer['position'],
                                                                        scale=layer['scale'],
                                                                        dnd_scale=layer['dndScale'],
                                                                        is_hidden=layer['is_hidden']))


def combine_fusion_handler(user_product_id, seller_id, sides, layer_by_side_dict, artwork_id_list,
                           artwork_fusion_infos_to_create, user_product_artwork_fusions_to_create):
    artwork_fusion = ArtworkFusion.objects.create(name=str(user_product_id) + str("_combine"),
                                                  owner_id=seller_id,
                                                  background_color=None)
    for side in sides:
        side_id = side.id
        content_by_side = layer_by_side_dict.get(side_id)
        artwork_fusion_info_handler(content_by_side, artwork_id_list, artwork_fusion, artwork_fusion_infos_to_create)

    user_product_artwork_fusions_to_create.append(UserProductArtworkFusion(user_product_id=user_product_id,
                                                                           product_side_id=sides[0].id,
                                                                           artwork_fusion=artwork_fusion))


def no_combine_fusion_handler(user_product_id, seller_id, sides, layer_by_side_dict, artwork_id_list,
                              artwork_fusion_infos_to_create, user_product_artwork_fusions_to_create,
                              artwork_fusions_to_create, sides_has_content, send_to_fulfill):
    for side in sides:
        side_id = side.id
        content_by_side = layer_by_side_dict.get(side_id)
        fusion_background_color = content_by_side[
            'backgroundColor'] if side.enable_background_color and 'backgroundColor' in content_by_side else None
        if content_by_side or side.fulfill_require_artwork:
            artwork_fusions_to_create.append(ArtworkFusion(name=str(user_product_id) + str(side_id),
                                                           owner_id=seller_id,
                                                           background_color=fusion_background_color))
            sides_has_content.append(side_id)

    created_artwork_fusions = ArtworkFusion.objects.bulk_create(artwork_fusions_to_create)

    for side_index, side_id in enumerate(sides_has_content):
        content_by_side = layer_by_side_dict.get(side_id)
        artwork_fusion = created_artwork_fusions[side_index]
        artwork_fusion_info_handler(content_by_side, artwork_id_list, artwork_fusion, artwork_fusion_infos_to_create)
        user_product_artwork_fusions_to_create.append(UserProductArtworkFusion(user_product_id=user_product_id,
                                                                               product_side_id=side_id,
                                                                               artwork_fusion=artwork_fusion,
                                                                               send_to_fulfill=send_to_fulfill))
