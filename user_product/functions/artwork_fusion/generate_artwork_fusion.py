import logging

from django.contrib.auth import get_user_model
from django.core.files.storage import get_storage_class

from service_communication.services.mockup_generator_service.artwork_fusion import \
    MockupArtworkFusionCommunicationService
from user_product.constants import FusionType, LayerType
from .retrieve_artwork_info import retrieve_layer_info

logger = logging.getLogger(__name__)
User = get_user_model()
media_storage = get_storage_class()()

THUMBNAIL_MAX_SIZE = float(1000)


def generate_product_artwork_fusion(user_product_artwork_fusion):
    request_data = generate_fusion_request_data(user_product_artwork_fusion, FusionType.FULFILL)
    MockupArtworkFusionCommunicationService.generate_artwork_fusion(user_product_artwork_fusion, request_data)


def generate_fusion_request_data(user_product_artwork_fusion, fusion_type=FusionType.GENERATE_MOCKUP):
    artwork_fusion = user_product_artwork_fusion.artwork_fusion
    background_color = artwork_fusion.background_color
    abstract_product = user_product_artwork_fusion.user_product.abstract_product
    side = user_product_artwork_fusion.product_side
    if "Pocket T-Shirt" in abstract_product.title:
        type = "pocket-tshirt"
        mockup_info = abstract_product.mockup_infos.first()
        mockup_info__preview = mockup_info.preview['Front']
        fusion_size = side.fusion_size
        fusion_width = fusion_size['artwork_fusion_size']['width']
        fusion_height = fusion_size['artwork_fusion_size']['height']
        preview_width = mockup_info__preview['image_width']
        scale = fusion_width / preview_width

        preview_artwork_frame_x = int(mockup_info__preview['frame_x'] * scale)
        preview_artwork_frame_y = int(mockup_info__preview['frame_y'] * scale)

        frame_x_to_fusion_center = preview_artwork_frame_x - fusion_width / 2
        frame_y_to_fusion_center = preview_artwork_frame_y - fusion_height / 2
        mockup_info__preview.update({
            "frame_x_to_fusion_center": frame_x_to_fusion_center,
            "frame_y_to_fusion_center": frame_y_to_fusion_center,
            "fusion_frame_scale": scale
        })

    else:
        type = "normal"
        mockup_info__preview = {}

    artwork_infos = retrieve_layer_infos_by_fusion(artwork_fusion=artwork_fusion)
    fusion_size = side.fusion_size["artwork_fusion_size"]
    request_data = {
        "type": type,
        "background_color": background_color,
        "mockup_info__preview": mockup_info__preview,
        "fusion_size": fusion_size,
        "artwork_infos": artwork_infos,
        "name": artwork_fusion.name,
        "scale": 1,
        "generate_thumbnail": True,
        "fusion_type": fusion_type,
        "combine_fusion": False,
        "fusion_meta": abstract_product.meta.fusion_meta
    }

    return request_data


def retrieve_layer_infos_by_fusion(artwork_fusion):
    layer_infos = []
    for artwork_info in artwork_fusion.artwork_fusion_info_artwork_set.is_visible():
        layer_content = artwork_info.layer_content
        layer_data = retrieve_layer_info(layer_content=layer_content, layer_info=artwork_info)
        layer_infos.append(layer_data)

    return layer_infos
