import logging

from shop.serializers import MerchantServiceShopSerializer

logger = logging.getLogger(__name__)


def generate_data_for_delete_adapter(shop):
    try:
        # logger.info("generate_data_for_delete_adapter...")
        shop_info = MerchantServiceShopSerializer(shop).data
        request_data = {
            **shop_info
        }

    except Exception as e:
        logger.exception(e)
        raise Exception(e)
    else:
        return request_data
