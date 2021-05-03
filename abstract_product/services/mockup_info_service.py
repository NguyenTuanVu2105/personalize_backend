from HUB.services import gs_image_service
from HUB.services.gs_file_service import gs_file_service
from HUB.settings import PRODUCT_CUT_IMAGE_DIRECTORY, PRODUCT_MODEL_DIRECTORY


def get_cut_image_download_url(path):
    return gs_image_service.convert_private_file_path_to_signed_url(f'{PRODUCT_CUT_IMAGE_DIRECTORY}/{path}')


def upload_cut_image(image, filename, mockup_info, side_index, part_index):
    consistency_name = mockup_info.meta.get('consistency_name')
    side_name = mockup_info.meta['mockup_infos'][side_index]['side'].lower()

    filename_with_folder = f'cut/{side_name}/{filename}'

    gs_image_service.upload_private_image(
        f'{PRODUCT_CUT_IMAGE_DIRECTORY}/{consistency_name}/{filename_with_folder}', image)

    mockup_info.meta['mockup_infos'][side_index]['parts'][part_index][
        'image_path'] = filename_with_folder
    mockup_info.save()
    return mockup_info


def get_model_file_download_url(path):
    return gs_file_service.convert_private_file_path_to_signed_url(f'{PRODUCT_MODEL_DIRECTORY}/{path}')


def upload_model_file(file, filename, mockup_info, side_index, part_index):
    gs_file_service.upload_private_file(f'{PRODUCT_MODEL_DIRECTORY}/{filename}', file)
    mockup_info.meta['mockup_infos'][side_index]['parts'][part_index][
        'model'] = filename
    mockup_info.save()
    return mockup_info
