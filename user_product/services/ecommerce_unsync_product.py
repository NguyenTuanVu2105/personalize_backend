from HUB.settings import LIMIT_GET_ECOMERCE_PRODUCT
from service_communication.services.adapter_services import AdapterProductCommunicationService


def get_all_product_in_store(shop):
    products = []
    since_id = None
    while True:
        resp = AdapterProductCommunicationService.get_product(shop, since_id=since_id)
        if 'products' not in resp:
            break
        since_id = resp['products'][-1]['id']
        products.extend(resp['products'])
        if len(resp['products']) < LIMIT_GET_ECOMERCE_PRODUCT:
            break
    return products
