import logging

from abstract_product.models import AbstractProduct

logger = logging.getLogger(__name__)


def mockup_preview_data_generator(product_id, mockup_version=None):
    abstract_product = AbstractProduct.objects.get(id=product_id)
    active_mockup_version = mockup_version if mockup_version else abstract_product.active_mockup_version
    data = {
        "colors": abstract_product.get_colors(),
    }

    mockup_infos_meta_data = {}
    consistency_name = ''
    artwork_side_info = ''
    for mockup_info in abstract_product.mockup_infos.all():
        mockup_info_id = mockup_info.id
        mockup_infos_meta = mockup_info.meta
        mockup_infos__preview_meta = mockup_info.preview_meta
        consistency_name = mockup_infos_meta['consistency_name']
        artwork_side_info = mockup_infos_meta['artwork_side_info']
        meta__mockup_infos = mockup_infos_meta['mockup_infos']
        if type(meta__mockup_infos).__name__ == 'dict' and active_mockup_version in meta__mockup_infos:
            active_mockup_info = meta__mockup_infos[active_mockup_version]
            for mockup_infos_meta__mockup_info in active_mockup_info:
                mockup_infos_meta__mockup_info.update({
                    "mockup_info_id": mockup_info_id,
                    "color_attr_interactive": mockup_infos__preview_meta['color_attr_interactive'],
                    "variant_color_attr": mockup_info.variants.first().get_color_value()
                })
            if active_mockup_version in mockup_infos_meta_data:
                mockup_infos_meta_data[active_mockup_version] = mockup_infos_meta_data[
                                                                    active_mockup_version] + active_mockup_info
            else:
                mockup_infos_meta_data[active_mockup_version] = active_mockup_info
        else:
            meta__mockup_infos = mockup_infos_meta['mockup_infos']
            for mockup_infos_meta__mockup_info in meta__mockup_infos:
                mockup_infos_meta__mockup_info.update({
                    "mockup_info_id": mockup_info_id,
                    "color_attr_interactive": mockup_infos__preview_meta['color_attr_interactive'],
                    "variant_color_attr": mockup_info.variants.first().get_color_value()
                })

            if "v1" not in mockup_infos_meta_data:
                mockup_infos_meta_data["v1"] = meta__mockup_infos
            else:
                mockup_infos_meta_data["v1"] = mockup_infos_meta_data["v1"] + meta__mockup_infos

    prefix_name = abstract_product.title.lower().replace('\'', '').replace(' ', '_')
    data.update({
        "prefix_name": prefix_name,
        "mockup_infos": mockup_infos_meta_data,
        "consistency_name": consistency_name,
        "artwork_side_info": artwork_side_info,
    })

    return data
