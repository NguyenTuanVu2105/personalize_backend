import logging
from service_communication.services.adapter_services import AdapterProductCommunicationService, \
    AdapterShopProductSyncCommunicationService
from shop.constants.shop_status import ShopStatus
from user_product.functions import adapter_request_data, generate_data_for_delete_adapter

logger = logging.getLogger(__name__)


def create_product_in_shop(shop_user_product):
    if shop_user_product.shop.status != ShopStatus.ACTIVE:
        return
    data = adapter_request_data(shop_user_product.user_product, shop_user_product.shop, shop_user_product)
    AdapterProductCommunicationService.new_product(shop_user_product, data)


def sync_product_in_shop(shop_user_product):
    if shop_user_product.shop.status != ShopStatus.ACTIVE:
        return
    data = adapter_request_data(shop_user_product.user_product, shop_user_product.shop, shop_user_product)
    AdapterShopProductSyncCommunicationService.new_product(shop_user_product, data)


