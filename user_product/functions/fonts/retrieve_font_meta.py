import logging
import traceback
import urllib
from io import BytesIO
from itertools import groupby
from operator import itemgetter

from django.conf import settings
from django.utils import timezone
from fontTools.ttLib import TTFont

from user_product.services.user_file_service import font_service

logger = logging.getLogger(__name__)


def retrieve_available_characters(file=None, file_url=None):
    try:
        if file:
            logger.info(f"File: {file}")
            font = TTFont(file)
        else:
            logger.info(f"File URL: {file_url}")
            with urllib.request.urlopen(file_url) as file_data:
                f = BytesIO(file_data.read())
                font = TTFont(f)

        unicode_list = []
        for character_code in font['cmap'].tables:
            if character_code.isUnicode():
                unicode_list = list(character_code.cmap.keys())
                break

        unicode_list = split_range(unicode_list)
        return unicode_list

    except Exception as e:
        logger.error("Failed to read FONT file!")
        logger.error(str(e))
        logger.exception(e)
        traceback.print_tb(e.__traceback__)
        raise Exception


def retrieve_font_meta(file, user):
    try:
        # file_extension = os.path.splitext(file.name)[1].strip(".")
        # prefix = f'{user.id}_{file.name.replace(f".{file_extension}", "")}'
        # font_url = font_service.upload_file(file_name_prefix=prefix, file_extension=file_extension, file_data=file)

        millis_timestamp = int(timezone.now().timestamp() * 1000)
        output_file_path = f'{settings.USER_FONT}/{user.id}_{millis_timestamp}_{file.name}'
        unicode_list = retrieve_available_characters(file=file)
        font_url = font_service.upload_public_file(file=file, output_file_path=output_file_path)
        return font_url, unicode_list

    except Exception as e:
        logger.error(str(e))
        raise Exception


def split_range(input_list):
    result = []
    for k, g in groupby(enumerate(input_list), lambda ix: ix[0] - ix[1]):
        item = list(map(itemgetter(1), g))
        if len(item) > 1:
            item = [item[0], item[-1]]
        result.append(item)
    return result

# from user_product.models import UserFontFamily
# from user_product.functions.fonts.retrieve_font_meta import retrieve_font_meta, retrieve_available_characters
# for queryset in UserFontFamily.objects.filter(is_active=True):
#     unicodes = retrieve_available_characters(file_url=queryset.font_url)
#     queryset.available_characters = unicodes
#     queryset.save()
