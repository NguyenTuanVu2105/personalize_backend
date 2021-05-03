from service_communication.constants.request_type import RequestType
from service_communication.services.adapter_services.adapter_shop_communication_service import \
    AdapterShopCommunicationService
from service_communication.services.webhook_job_services import WebhookJobCallbackService, WebhookJobRecoveryService
from shop.constants.shop_location_type import ShopLocationType
from shop.models import Shop, ShopLocationChange

check_shop_location_request_type = RequestType.ADAPTER_CHECK_SHOP_LOCATION

import logging

logger = logging.getLogger(__name__)


def check_shop_location_successful_callback(shop, response):
    # logger.info(response)
    has_location = response.get('has_location')
    if not has_location:
        ShopLocationChange.objects.update_or_create(shop=shop,  type=ShopLocationType.NOT_HAS_LOCATION,
                                                    defaults={
                                                        "shopify_response":response,
                                                        "is_resolve": False
                                                    })
    else:
        same_location = response.get('same_location')
        new_location = response.get('shop_location')
        old_location = response.get('app_location')
        if not same_location:
            ShopLocationChange.objects.create(shop=shop, type=ShopLocationType.WRONG_LOCATION,
                                              defaults = {
                                                  "shopify_response": response,
                                                  "new_location": new_location,
                                                  "old_location": old_location,
                                                  "is_resolve": False
                                              })


def check_shop_location_failed_callback(shop, response):
    logger.info(response)


def build_check_shop_location_from_shop_id_function(function):
    def get_objs_and_pass_to_function(shop_id):
        shop_obj = Shop.objects.filter(id=shop_id).first()
        if shop_obj:
            function(shop_obj)

    return get_objs_and_pass_to_function


post_check_shop_location_from_shop_id = build_check_shop_location_from_shop_id_function(AdapterShopCommunicationService.check_location)
WebhookJobCallbackService.register_callbacks(request_type=check_shop_location_request_type,
                                             callbacks=(
                                                 check_shop_location_successful_callback,
                                                 check_shop_location_failed_callback))

WebhookJobRecoveryService.register_function(request_type=check_shop_location_request_type,
                                            function=(post_check_shop_location_from_shop_id))
