import logging

from django.contrib.auth import get_user_model
from django.core.files.storage import get_storage_class

from service_communication.services.mockup_generator_service.artwork_fusion import \
    MockupArtworkFusionCommunicationService
from user_product.constants import FusionType
from .retrieve_artwork_info import retrieve_layer_info

logger = logging.getLogger(__name__)
User = get_user_model()
media_storage = get_storage_class()()

THUMBNAIL_MAX_SIZE = float(1000)


def generate_product_combined_artwork_fusion(user_product, separated_side_user_product_artwork_fusions,
                                             fulfill_user_product_artwork_fusion):
    request_data = retrieve_combined_fusion_request_data(user_product, separated_side_user_product_artwork_fusions,
                                                         fulfill_user_product_artwork_fusion)
    MockupArtworkFusionCommunicationService.generate_artwork_fusion(fulfill_user_product_artwork_fusion, request_data)


def retrieve_combined_fusion_request_data(user_product, separated_side_user_product_artwork_fusions,
                                          fulfill_user_product_artwork_fusion):
    fulfill_artwork_fusion = fulfill_user_product_artwork_fusion.artwork_fusion
    abstract_product = user_product.abstract_product
    side_fusion_infos = []

    for user_product_artwork_fusion in separated_side_user_product_artwork_fusions:
        side = user_product_artwork_fusion.product_side
        artwork_fusion = user_product_artwork_fusion.artwork_fusion
        side_fusion_infos.append({
            "side": side.type,
            "fusion_size": side.fusion_size["artwork_fusion_size"],
            "background_color": artwork_fusion.background_color or user_product.background_color,
            "artwork_infos": retrieve_artwork_infos(artwork_fusion),
        })

    request_data = {
        "combine_fusion": True,
        "side_fusion_infos": side_fusion_infos,
        "name": fulfill_artwork_fusion.name,
        "generate_thumbnail": True,
        "fusion_type": FusionType.FULFILL,
        "fusion_meta": abstract_product.meta.fusion_meta,
    }

    return request_data


def retrieve_artwork_infos(artwork_fusion):
    layer_infos = []
    for artwork_fusion_info in artwork_fusion.artwork_fusion_info_artwork_set.is_visible():
        layer_content = artwork_fusion_info.layer_content
        layer_data = retrieve_layer_info(layer_content=layer_content, layer_info=artwork_fusion_info)
        layer_infos.append(layer_data)
    return layer_infos
