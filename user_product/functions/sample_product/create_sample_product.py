import logging
import traceback

from helper.datetime_helpers import get_current_datetime
from user_product.functions import retrieve_user_product_variant
from user_product.models import SampleProduct
from user_product.serializers.sample_product import SPUserProductSerializer

logger = logging.getLogger(__name__)


def create_sample_product(user_product):
    try:
        preview_image_url = user_product.preview_image_url
        title = user_product.title
        user_product_data = SPUserProductSerializer(instance=user_product).data
        variant_list = retrieve_user_product_variant(user_product=user_product)
        created_sample_product = SampleProduct.objects.create(original_product=user_product, title=title,
                                                              preview_image_url=preview_image_url,
                                                              variant_list=variant_list,
                                                              detail_data=user_product_data)

        return created_sample_product.id, True

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
        return None, False


def update_sample_product(sample_product):
    try:
        user_product = sample_product.original_product
        sample_product.preview_image_url = user_product.preview_image_url
        sample_product.title = user_product.title
        sample_product.detail_data = SPUserProductSerializer(instance=user_product).data
        sample_product.variant_list = retrieve_user_product_variant(user_product=user_product)
        sample_product.last_refresh_data_time = get_current_datetime()
        sample_product.save()
        return sample_product.id

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.info(str(e))
        return None
