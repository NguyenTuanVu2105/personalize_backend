from user_product.constants.artwork_fusion_info_metas import LayerType
from user_product.serializers import MockupTextPersonalizationSerializer


def retrieve_layer_info(layer_content, layer_info):
    layer_result = None

    if layer_info.layer_type == LayerType.ARTWORK:
        layer_result = {
            "layer_type": layer_info.layer_type,
            "original_image_path": layer_content.original_image_path,
            "name": layer_content.name,
            "id": layer_content.id,
            "position": layer_info.position,
            "scale": float(layer_info.scale),
            "dnd_scale": float(layer_info.dnd_scale),
            "rotation": float(layer_info.rotation),
            "width": layer_content.width,
            "height": layer_content.height,
            "layer": layer_info.layer
        }

    elif layer_info.layer_type == LayerType.PERSONAL_TEXT:
        layer_content_data = MockupTextPersonalizationSerializer(instance=layer_content).data
        layer_result = {
            "layer_type": layer_info.layer_type,
            "position": layer_info.position,
            "scale": float(layer_info.scale),
            "dnd_scale": float(layer_info.dnd_scale),
            "rotation": float(layer_info.rotation),
            "layer": layer_info.layer,
            **layer_content_data
        }

    return layer_result
