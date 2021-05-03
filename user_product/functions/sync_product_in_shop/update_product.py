from service_communication.services.adapter_services import AdapterProductCommunicationService
from shop.constants.shop_status import ShopStatus
from user_product.functions import adapter_request_data


def update_product_in_shop(shop_user_product):
    if shop_user_product.shop.status != ShopStatus.ACTIVE:
        return
    data = adapter_request_data(shop_user_product.user_product, shop_user_product.shop, shop_user_product)
    AdapterProductCommunicationService.update_product(shop_user_product, data)